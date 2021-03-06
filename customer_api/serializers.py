from rest_framework import serializers
from .models import Customer, ServiceOrder, OrderProduct, CustomerLatePay, CustomerLoyaltyPointScheme
from users.serializers import SalespersonDetailSerializer
from asset_api.serializers import SOProductDetailsSerializer
from salesperson_api.models import LeaderboardPointSchema, Leaderboard, SalespersonLocation
from asset_api.models import VehicleProduct, VehicleSalesperson
import decimal


class CustomerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ['created_by']

    def validate(self, attrs):
        contact_no = attrs.get('contact_no', '')

        if len(contact_no) < 10:
            raise serializers.ValidationError('The contact number is invalid')
        return attrs


# this to specify what attrs required in the service order list
class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['shop_name', 'owner_first_name', 'owner_last_name', 'profile_picture', ]


class OrderProductItemSerializer(serializers.ModelSerializer):
    product = SOProductDetailsSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'price_at_the_time']


class ServiceOrderViewSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer()
    salesperson = SalespersonDetailSerializer()

    order_items = OrderProductItemSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        extra_fields = ['order_items']
        model = ServiceOrder
        # this will automatically resolve all the onetoone fields
        # depth = 1


# serializers to create so
class OrderProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        exclude = ['order']


class CreateServiceOrderSerializer(serializers.ModelSerializer):
    PAYMENT_OPTION = [('later', 'later'), ('now', 'now')]
    order_items = OrderProductCreateSerializer(many=True)
    so_type = serializers.ChoiceField(choices=PAYMENT_OPTION, write_only=True)

    class Meta:
        model = ServiceOrder
        exclude = ['salesperson']
        extra_fields = ['order_items', 'so_type']

    def create(self, validated_data):
        order_data = validated_data.pop('order_items')

        # get payment type
        so_type = validated_data.pop('so_type')
        so = ServiceOrder.objects.create(**validated_data)

        # get vehicle salesperson obj
        v_sp = VehicleSalesperson.objects.get(salesperson=so.salesperson)

        for item in order_data:
            vehicle_prod = VehicleProduct.objects.get(product=item['product'].id, vehicle_salesperson=v_sp)

            if vehicle_prod.quantity < item['quantity']:
                so.original_price -= item['quantity'] * item['price_at_the_time']
                so.save()
                raise serializers.ValidationError("Quantity requested is not in stocks.")

            OrderProduct.objects.create(order=so, **item)

            vehicle_prod.quantity -= item['quantity']
            vehicle_prod.save()

        #     get leaderboard obj
        lb_object = Leaderboard.objects.get(salesperson=so.salesperson)

        if so_type == 'later':
            schema = LeaderboardPointSchema.objects.get(points_type='SO_PAY_LATER')
            points = schema.bonus_points + decimal.Decimal(
                so.original_price) * schema.percentage / 100
            lb_object.points_today += points
            lb_object.points_current_month += points
            lb_object.points_all_time += points
            lb_object.save()
            #     add outstanding to the customer
            customer = Customer.objects.get(id=so.customer_id)
            customer.outstanding += so.original_price
            customer.save()

        else:
            schema = LeaderboardPointSchema.objects.get(points_type='SO_PAY')
            points = schema.bonus_points + decimal.Decimal(
                so.original_price) * schema.percentage / 100
            lb_object.points_today += points
            lb_object.points_current_month += points
            lb_object.points_all_time += points
            lb_object.save()
            #     deduct loyalty points
            customer = Customer.objects.get(id=so.customer_id)
            customer.loyalty_points -= so.discount
            customer.save()

        SalespersonLocation.objects.create(customer=so.customer, salesperson=so.salesperson)
        return so


# customer search serializer


class CustomerSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['created_by']


# customer late pay related
class CustomerLatePayListViewSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer()
    salesperson = SalespersonDetailSerializer()

    class Meta:
        model = CustomerLatePay
        fields = '__all__'


# post customer late pay serializer
class CustomerLatePayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLatePay
        exclude = ['salesperson']


class CustomerLatePayViewSerializer(serializers.ModelSerializer):
    salesperson = SalespersonDetailSerializer()

    class Meta:
        model = CustomerLatePay
        fields = '__all__'


# update loyalty points
class LoyaltyPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoyaltyPointScheme
        fields = '__all__'


class LoyaltyPointSchemaViewSerializer(serializers.ModelSerializer):
    points_type = serializers.CharField(source='get_points_type_display')

    class Meta:
        model = CustomerLoyaltyPointScheme
        fields = '__all__'

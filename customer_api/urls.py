from .views import CustomerListView, CustomerView, ServiceOrderListView, ServiceOrderView, CustomerServiceOrdersView, \
    CreateServiceOrderView, SearchCustomerView, CustomerLatePayView, CreateLatePayView, AllCustomerLatePayView, \
    CreateLoyaltyPointsView, DeleteLoyaltyPointsView, LoyaltyPointSchemaView, UpdateLoyaltyPointSchema
from django.urls import path

app_name = 'customer'

urlpatterns = [
    path('', CustomerListView.as_view(), name='all-customers'),
    path('<int:id>', CustomerView.as_view(), name='single-customer'),
    path('search/', SearchCustomerView.as_view(), name='search-customer'),
    path('service-orders/', ServiceOrderListView.as_view(), name='all-so'),
    path('service-orders/create', CreateServiceOrderView.as_view(), name='create-so'),
    path('service-orders/<int:id>', ServiceOrderView.as_view(), name='get-so'),
    path('service-orders/cus/<int:id>', CustomerServiceOrdersView.as_view(), name='all-customer-so'),
    path('late-payment/', AllCustomerLatePayView.as_view(), name='all-late-pay'),
    path('late-payment/pay', CreateLatePayView.as_view(), name='add-late-pay'),
    path('late-payment/cus/<int:id>', CustomerLatePayView.as_view(), name='per-customer-late-pay'),
    path('loaylty-points/', CreateLoyaltyPointsView.as_view(), name='create-loyalty-points'),
    path('loaylty-points/<int:pk>', DeleteLoyaltyPointsView.as_view(), name='delete-loyalty-points'),
    path('loyalty-point-schema/', LoyaltyPointSchemaView.as_view(), name='loyalty-point-schema'),
    path('loyalty-point-schema/<int:id>', UpdateLoyaltyPointSchema.as_view(),
         name='update-loyalty-point-schema'),

]

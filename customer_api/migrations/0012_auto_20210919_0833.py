# Generated by Django 3.2.6 on 2021-09-19 03:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer_api', '0011_auto_20210918_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='district',
            field=models.CharField(choices=[('Ampara', 'Ampara'), ('Trincomalee', 'Trincomalee'), ('Gampaha', 'Gampaha'), ('Kegalle', 'Kegalle'), ('Hambantota', 'Hambantota'), ('Kilinochchi', 'Kilinochchi'), ('Nuwara Eliya', 'Nuwara Eliya'), ('Puttalam', 'Puttalam'), ('Ratnapura', 'Ratnapura'), ('Monaragala', 'Monaragala'), ('Kurunegala', 'Kurunegala'), ('Polonnaruwa', 'Polonnaruwa'), ('Matara', 'Matara'), ('Colombo', 'Colombo'), ('Matale', 'Matale'), ('Kalutara', 'Kalutara'), ('Mannar', 'Mannar'), ('Batticaloa', 'Batticaloa'), ('Badulla', 'Badulla'), ('Vavuniya', 'Vavuniya'), ('Anuradhapura', 'Anuradhapura'), ('Mullaitivu', 'Mullaitivu'), ('Galle', 'Galle'), ('Kandy', 'Kandy'), ('Jaffna', 'Jaffna')], max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='shop_name',
            field=models.CharField(db_index=True, max_length=225),
        ),
        migrations.CreateModel(
            name='CustomerLatePay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='late_pay_customer', to='customer_api.customer')),
                ('salesperson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='late_pay_sp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 3.2.6 on 2021-09-24 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset_api', '0015_alter_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleproduct',
            name='assigned_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products_assigner', to='users.staff'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, max_length=255, upload_to='product/'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('VAN', 'Van'), ('CAB', 'cab'), ('LORRY', 'Lorry'), ('BIKE', 'bike'), ('THREEWHEELER', 'threewheeler')], max_length=150),
        ),
    ]
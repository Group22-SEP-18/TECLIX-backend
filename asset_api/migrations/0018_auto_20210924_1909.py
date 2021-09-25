# Generated by Django 3.2.6 on 2021-09-24 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_api', '0017_auto_20210924_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicleproduct',
            options={'ordering': ['vehicle_salesperson']},
        ),
        migrations.AddField(
            model_name='vehicleproduct',
            name='vehicle_salesperson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_vehicle', to='asset_api.vehiclesalesperson'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('cake', 'Cake'), ('biscuit', 'Biscuit')], max_length=150),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('CAB', 'cab'), ('LORRY', 'Lorry'), ('VAN', 'Van'), ('THREEWHEELER', 'threewheeler'), ('BIKE', 'bike')], max_length=150),
        ),
        migrations.AlterUniqueTogether(
            name='vehicleproduct',
            unique_together={('vehicle_salesperson', 'product')},
        ),
        migrations.RemoveField(
            model_name='vehicleproduct',
            name='assigned_by',
        ),
        migrations.RemoveField(
            model_name='vehicleproduct',
            name='vehicle',
        ),
    ]
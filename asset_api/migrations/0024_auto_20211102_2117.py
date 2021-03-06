# Generated by Django 3.2.6 on 2021-11-02 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_api', '0023_auto_20211102_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('snacks', 'Snacks'), ('cookies', 'Cookies'), ('cheese', 'Cheese'), ('biscuit', 'Biscuit'), ('sauce', 'Sauce'), ('chips', 'Chips')], max_length=150),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('LORRY', 'Lorry'), ('VAN', 'Van'), ('BIKE', 'Bike'), ('TUK', 'Tuk')], max_length=150),
        ),
    ]

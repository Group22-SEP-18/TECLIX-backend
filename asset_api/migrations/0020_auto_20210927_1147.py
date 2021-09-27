# Generated by Django 3.2.6 on 2021-09-27 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_api', '0019_auto_20210927_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(db_index=True, default='unknown', max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('BIKE', 'bike'), ('LORRY', 'Lorry'), ('THREEWHEELER', 'threewheeler'), ('VAN', 'Van'), ('CAB', 'cab')], max_length=150),
        ),
    ]

# Generated by Django 3.2.6 on 2021-09-20 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesperson_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salespersonlocation',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='salespersonlocation',
            old_name='salesperson_id',
            new_name='salesperson',
        ),
        migrations.AlterField(
            model_name='salespersonlocation',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

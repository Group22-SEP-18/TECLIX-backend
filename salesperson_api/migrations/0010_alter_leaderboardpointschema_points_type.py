# Generated by Django 3.2.6 on 2021-09-22 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesperson_api', '0009_alter_leaderboardpointschema_points_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboardpointschema',
            name='points_type',
            field=models.CharField(choices=[('ITEM_COUNT', 'Item Count'), ('LATE_PAYMENTS', 'Late Payments'), ('SO', 'Service Orders')], max_length=100),
        ),
    ]

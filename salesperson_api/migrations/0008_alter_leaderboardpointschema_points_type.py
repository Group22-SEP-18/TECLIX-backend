# Generated by Django 3.2.6 on 2021-09-22 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesperson_api', '0007_alter_leaderboardpointschema_points_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboardpointschema',
            name='points_type',
            field=models.CharField(choices=[('LATE_PAYMENTS', 'Late Payments'), ('SO', 'Service Orders'), ('ITEM_COUNT', 'Item Count')], max_length=100),
        ),
    ]

# Generated by Django 3.2.6 on 2021-09-20 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesperson_api', '0004_leaderboardpointschema'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboard',
            name='points_all_time',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='points_current_month',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='leaderboard',
            name='points_today',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='leaderboardpointschema',
            name='points_type',
            field=models.CharField(choices=[('LATE_PAYMENTS', 'Late Payments'), ('ITEM_COUNT', 'Item Count'), ('SO', 'Service Orders')], max_length=100),
        ),
    ]

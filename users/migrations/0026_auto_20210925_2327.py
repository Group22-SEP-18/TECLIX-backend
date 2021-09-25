# Generated by Django 3.2.6 on 2021-09-25 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_merge_20210924_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='staff',
            name='user_role',
            field=models.CharField(choices=[('OFFICER', 'Distribution Officer'), ('MANAGER', 'Operations Manager'), ('SALESPERSON', 'Salesperson')], max_length=50),
        ),
    ]
# Generated by Django 3.2.6 on 2021-08-10 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_staff_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]

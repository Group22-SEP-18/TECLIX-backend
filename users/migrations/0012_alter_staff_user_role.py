# Generated by Django 3.2.6 on 2021-09-18 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_staff_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='user_role',
            field=models.CharField(choices=[('SALESPERSON', 'Salesperson'), ('MANAGER', 'Operations Manager'), ('OFFICER', 'Distribution Officer')], max_length=50),
        ),
    ]

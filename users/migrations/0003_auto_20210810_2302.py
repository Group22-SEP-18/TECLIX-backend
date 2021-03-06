# Generated by Django 3.2.6 on 2021-08-10 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_staff_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='profile_picture',
            field=models.ImageField(max_length=300, upload_to='staff/'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='user_role',
            field=models.CharField(choices=[('MANAGER', 'Operations Manager'), ('SALESPERSON', 'Salesperson'), ('OFFICER', 'Distribution Officer')], max_length=50),
        ),
    ]

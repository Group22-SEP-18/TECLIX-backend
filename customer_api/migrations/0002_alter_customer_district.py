# Generated by Django 3.2.6 on 2021-09-18 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='district',
            field=models.CharField(choices=[('Anuradhapura', 'Anuradhapura'), ('Ampara', 'Ampara'), ('Puttalam', 'Puttalam'), ('Kegalle', 'Kegalle'), ('Kalutara', 'Kalutara'), ('Matara', 'Matara'), ('Kandy', 'Kandy'), ('Monaragala', 'Monaragala'), ('Polonnaruwa', 'Polonnaruwa'), ('Mannar', 'Mannar'), ('Mullaitivu', 'Mullaitivu'), ('Kurunegala', 'Kurunegala'), ('Badulla', 'Badulla'), ('Hambantota', 'Hambantota'), ('Nuwara Eliya', 'Nuwara Eliya'), ('Colombo', 'Colombo'), ('Gampaha', 'Gampaha'), ('Trincomalee', 'Trincomalee'), ('Ratnapura', 'Ratnapura'), ('Galle', 'Galle'), ('Kilinochchi', 'Kilinochchi'), ('Matale', 'Matale'), ('Batticaloa', 'Batticaloa'), ('Jaffna', 'Jaffna'), ('Vavuniya', 'Vavuniya')], max_length=100),
        ),
    ]

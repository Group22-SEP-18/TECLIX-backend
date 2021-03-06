# Generated by Django 3.2.6 on 2021-09-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_api', '0028_auto_20210926_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='district',
            field=models.CharField(choices=[('Ratnapura', 'Ratnapura'), ('Polonnaruwa', 'Polonnaruwa'), ('Mullaitivu', 'Mullaitivu'), ('Kegalle', 'Kegalle'), ('Monaragala', 'Monaragala'), ('Ampara', 'Ampara'), ('Vavuniya', 'Vavuniya'), ('Badulla', 'Badulla'), ('Matara', 'Matara'), ('Kandy', 'Kandy'), ('Anuradhapura', 'Anuradhapura'), ('Kalutara', 'Kalutara'), ('Colombo', 'Colombo'), ('Batticaloa', 'Batticaloa'), ('Kurunegala', 'Kurunegala'), ('Jaffna', 'Jaffna'), ('Nuwara Eliya', 'Nuwara Eliya'), ('Kilinochchi', 'Kilinochchi'), ('Hambantota', 'Hambantota'), ('Gampaha', 'Gampaha'), ('Galle', 'Galle'), ('Mannar', 'Mannar'), ('Matale', 'Matale'), ('Trincomalee', 'Trincomalee'), ('Puttalam', 'Puttalam')], max_length=100),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='order_date',
            field=models.DateField(auto_now=True),
        ),
    ]

# Generated by Django 3.2.6 on 2021-09-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_api', '0019_merge_20210920_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerloyaltypointscheme',
            name='max_amount',
            field=models.DecimalField(decimal_places=2, default=100000.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='customer',
            name='district',
            field=models.CharField(choices=[('Ratnapura', 'Ratnapura'), ('Colombo', 'Colombo'), ('Puttalam', 'Puttalam'), ('Galle', 'Galle'), ('Mannar', 'Mannar'), ('Badulla', 'Badulla'), ('Trincomalee', 'Trincomalee'), ('Matara', 'Matara'), ('Gampaha', 'Gampaha'), ('Anuradhapura', 'Anuradhapura'), ('Vavuniya', 'Vavuniya'), ('Kurunegala', 'Kurunegala'), ('Kilinochchi', 'Kilinochchi'), ('Mullaitivu', 'Mullaitivu'), ('Kalutara', 'Kalutara'), ('Ampara', 'Ampara'), ('Hambantota', 'Hambantota'), ('Kandy', 'Kandy'), ('Matale', 'Matale'), ('Jaffna', 'Jaffna'), ('Batticaloa', 'Batticaloa'), ('Kegalle', 'Kegalle'), ('Polonnaruwa', 'Polonnaruwa'), ('Monaragala', 'Monaragala'), ('Nuwara Eliya', 'Nuwara Eliya')], max_length=100),
        ),
        migrations.AlterField(
            model_name='customerloyaltypointscheme',
            name='minimum_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
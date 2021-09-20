from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_staff_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='user_role',
            field=models.CharField(choices=[('MANAGER', 'Operations Manager'), ('SALESPERSON', 'Salesperson'), ('OFFICER', 'Distribution Officer')], max_length=50),
        ),
    ]

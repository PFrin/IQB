# Generated by Django 4.1.5 on 2023-06-20 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_alter_customer_options_remove_customer_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='loginCust',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

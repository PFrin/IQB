# Generated by Django 4.1.5 on 2023-06-12 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_form_mepdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='MEPDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
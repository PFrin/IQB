# Generated by Django 4.1.5 on 2023-12-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='css_file',
        ),
        migrations.AddField(
            model_name='form',
            name='logo_path',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

# Generated by Django 4.1.5 on 2023-06-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_idquestion_answer_idanswer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='isOnline',
            field=models.BooleanField(default='False'),
        ),
    ]
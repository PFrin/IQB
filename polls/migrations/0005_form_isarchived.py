# Generated by Django 4.1.5 on 2024-02-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_rename_dependency_formula_question_dependency_formul'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='isArchived',
            field=models.BooleanField(default=False),
        ),
    ]
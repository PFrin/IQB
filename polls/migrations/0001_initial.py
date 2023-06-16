# Generated by Django 4.1.5 on 2023-06-09 08:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('idAnswer', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('Answer', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('idCustomer', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('mailCust', models.TextField(max_length=100)),
                ('loginCust', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('idForm', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('titleForm', models.TextField(max_length=100)),
                ('introText', models.TextField(default='Binevenue sur notre formulaire.', max_length=100)),
                ('concludingText', models.TextField(default="Merci d'avoir rempli notre formulaire.", max_length=100)),
                ('CreationDate', models.DateTimeField(auto_now_add=True)),
                ('MEPDate', models.DateTimeField()),
                ('lastModifiedDate', models.DateTimeField(auto_now=True)),
                ('isOnline', models.BooleanField(default='False')),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('idPage', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField()),
                ('Form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.form')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('idQuestion', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('title', models.TextField(max_length=100)),
                ('isObligatory', models.BooleanField()),
                ('nbrAnswerMin', models.IntegerField()),
                ('nbrAnswerMax', models.IntegerField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.page')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('idType', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('typeQuestion', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('idUSer', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('mailUser', models.TextField(max_length=100)),
                ('loginUser', models.CharField(max_length=100)),
                ('passwordUser', models.TextField(max_length=100)),
                ('replayDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('idUserAnswer', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('text', models.TextField(max_length=100)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.user')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.type'),
        ),
        migrations.AddField(
            model_name='answer',
            name='Question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.type'),
        ),
    ]

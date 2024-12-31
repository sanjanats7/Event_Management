# Generated by Django 5.0.6 on 2024-12-31 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='attendee',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='Enter a valid email address.')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d{10,15}$', 'Phone number must be between 10 and 15 digits.')]),
        ),
    ]
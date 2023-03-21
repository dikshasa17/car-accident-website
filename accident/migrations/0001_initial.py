# Generated by Django 3.2.4 on 2023-01-31 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('user_mobile', models.CharField(max_length=10)),
                ('user_email', models.EmailField(max_length=254)),
                ('vehicle_number_plate', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('addharcard', models.CharField(max_length=20)),
                ('bloodgrp', models.CharField(max_length=6)),
                ('image', models.ImageField(blank=True, upload_to='media/accident/images/')),
                ('emergency_no1', models.CharField(max_length=10)),
                ('emergency_no2', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datecompleted', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.2.4 on 2023-02-01 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accident', '0004_auto_20230201_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='emergency_no1',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='accident',
            name='emergency_no2',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='accident',
            name='user_mobile',
            field=models.CharField(max_length=10),
        ),
    ]

# Generated by Django 2.1.7 on 2019-03-14 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='613-555-555', max_length=20),
        ),
    ]

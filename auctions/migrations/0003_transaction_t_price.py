# Generated by Django 2.1.7 on 2019-03-16 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20190315_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='t_price',
            field=models.DecimalField(decimal_places=1, default=25.0, max_digits=10),
        ),
    ]
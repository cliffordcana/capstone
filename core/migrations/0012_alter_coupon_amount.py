# Generated by Django 4.0 on 2021-12-12 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='amount',
            field=models.IntegerField(choices=[(50, 50), (100, 100), (150, 150)], default=50),
        ),
    ]

# Generated by Django 4.0 on 2021-12-13 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_activitylog_coupon_alter_activitylog_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingorder',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]

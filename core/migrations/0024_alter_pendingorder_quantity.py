# Generated by Django 4.0 on 2021-12-14 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_transaction_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingorder',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
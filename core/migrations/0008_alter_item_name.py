# Generated by Django 4.0 on 2021-12-11 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_item_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]

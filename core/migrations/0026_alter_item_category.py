# Generated by Django 4.0 on 2021-12-15 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('BEVERAGE', 'BEVERAGE'), ('CANNED GOODS', 'CANNED GOODS'), ('DAIRY PRODUCTS', 'DAIRY PRODUCTS'), ('FROZEN FOODS', 'FROZEN FOODS'), ('PERSONAL CARE', 'PERSONAL CARE'), ('CLEANING MATERIAL', 'CLEANING MATERIAL')], default='BEVERAGE', max_length=17),
        ),
    ]
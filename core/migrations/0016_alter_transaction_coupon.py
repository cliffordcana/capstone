# Generated by Django 4.0 on 2021-12-12 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_pendingorder_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='core.coupon'),
        ),
    ]

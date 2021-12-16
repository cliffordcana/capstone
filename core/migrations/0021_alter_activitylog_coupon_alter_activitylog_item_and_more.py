# Generated by Django 4.0 on 2021-12-12 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_activitylog_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_log_coupon', to='core.coupon'),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_log_item', to='core.item'),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='pending_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_log_pending_order', to='core.pendingorder'),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_log_transaction', to='core.transaction'),
        ),
    ]

# Generated by Django 4.0 on 2021-12-12 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_activitylog_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

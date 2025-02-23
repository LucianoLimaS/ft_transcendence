# Generated by Django 5.1.4 on 2025-02-22 21:03

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0004_alter_chatgroup_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
    ]

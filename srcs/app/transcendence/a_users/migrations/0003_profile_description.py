# Generated by Django 5.1.4 on 2024-12-24 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0002_profile_created_at_profile_last_login_profile_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

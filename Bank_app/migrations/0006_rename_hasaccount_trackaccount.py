# Generated by Django 5.0 on 2024-01-18 01:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Bank_app", "0005_alter_hasaccount_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HasAccount",
            new_name="TrackAccount",
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-12 06:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="comment",
            new_name="introduce",
        ),
    ]
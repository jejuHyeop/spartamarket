# Generated by Django 5.0.4 on 2024-04-12 06:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="comment",
            field=models.TextField(blank=True),
        ),
    ]

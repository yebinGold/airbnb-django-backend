# Generated by Django 4.1.2 on 2022-11-18 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_photo",
            field=models.URLField(blank=True),
        ),
    ]

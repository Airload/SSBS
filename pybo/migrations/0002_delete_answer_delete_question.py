# Generated by Django 4.2.7 on 2023-12-18 01:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pybo", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Answer",
        ),
        migrations.DeleteModel(
            name="Question",
        ),
    ]
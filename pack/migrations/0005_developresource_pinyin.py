# Generated by Django 4.1.7 on 2023-03-11 03:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pack", "0004_alter_pack_pack_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="developresource",
            name="pinyin",
            field=models.CharField(max_length=40, null=True),
        ),
    ]

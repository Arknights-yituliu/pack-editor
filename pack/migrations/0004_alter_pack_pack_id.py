# Generated by Django 4.1.7 on 2023-03-10 01:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pack", "0003_alter_developresource_name_alter_gacharesource_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pack",
            name="pack_id",
            field=models.IntegerField(help_text="礼包ID", unique=True),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-10 01:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pack", "0002_alter_pack_on_sale_alter_pack_originium_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="developresource",
            name="name",
            field=models.CharField(help_text="名称", max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name="gacharesource",
            name="name",
            field=models.CharField(help_text="名称", max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name="otheritem",
            name="name",
            field=models.CharField(help_text="名称", max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name="pack",
            name="name",
            field=models.CharField(help_text="名称", max_length=40, unique=True),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-11 03:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pack", "0006_alter_developresource_pinyin"),
    ]

    operations = [
        migrations.AddField(
            model_name="gacharesource",
            name="value",
            field=models.FloatField(default=0, help_text="等效理智价值", null=True),
        ),
        migrations.AlterField(
            model_name="developresource",
            name="pinyin",
            field=models.CharField(help_text="拼音", max_length=40),
        ),
    ]
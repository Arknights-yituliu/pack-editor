# Generated by Django 4.1.7 on 2023-03-11 03:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pack", "0007_gacharesource_value_alter_developresource_pinyin"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gacharesource",
            name="value",
        ),
        migrations.AddField(
            model_name="developresource",
            name="value",
            field=models.FloatField(default=0, help_text="等效理智价值", null=True),
        ),
    ]
# Generated by Django 4.2.3 on 2023-07-31 01:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pack", "0004_alter_otheritem_originium_alter_pack_end_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pack",
            name="img",
            field=models.ImageField(blank=True, null=True, upload_to="pack_img"),
        ),
    ]

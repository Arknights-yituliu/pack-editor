# Generated by Django 4.1.7 on 2023-04-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pack", "0003_remove_pack_on_sale_pack_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="otheritem",
            name="originium",
            field=models.FloatField(help_text="等价源石"),
        ),
        migrations.AlterField(
            model_name="pack",
            name="end_date",
            field=models.DateField(blank=True, help_text="停售日期，留空时不检查停售日期", null=True),
        ),
        migrations.AlterField(
            model_name="pack",
            name="on_sale_control",
            field=models.CharField(
                choices=[("on", "在售（忽略时间）"), ("off", "停售（忽略时间）"), ("time", "自动（时间控制）")],
                default="time",
                help_text="若起始与结束日期均为空，则礼包永久在售",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="pack",
            name="start_date",
            field=models.DateField(blank=True, help_text="开售日期，留空时不检查开售日期", null=True),
        ),
    ]

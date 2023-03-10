# Generated by Django 4.1.7 on 2023-03-11 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DevelopList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="DevelopResource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(help_text="名称", max_length=40, unique=True)),
                ("pinyin", models.CharField(help_text="拼音", max_length=40)),
                ("value", models.FloatField(default=0, help_text="等效理智价值", null=True)),
            ],
        ),
        migrations.CreateModel(
            name="GachaList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="GachaResource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(help_text="名称", max_length=40, unique=True)),
                ("orundum", models.IntegerField(help_text="等价合成玉")),
            ],
        ),
        migrations.CreateModel(
            name="OtherItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(help_text="名称", max_length=40, unique=True)),
                ("originium", models.IntegerField(help_text="等价源石")),
            ],
        ),
        migrations.CreateModel(
            name="OtherList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField()),
                (
                    "other_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pack.otheritem"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(help_text="名称", max_length=40, unique=True)),
                ("pack_id", models.IntegerField(help_text="礼包ID", unique=True)),
                (
                    "limitation",
                    models.CharField(
                        choices=[
                            ("1", "once"),
                            ("m", "monthly"),
                            ("w", "weekly"),
                            ("y", "year"),
                            ("p", "permanent"),
                            ("l", "limited"),
                        ],
                        help_text="购买限制",
                        max_length=1,
                    ),
                ),
                ("price", models.IntegerField(help_text="价格（元）")),
                ("on_sale", models.BooleanField(default=True, help_text="是否在售")),
                ("originium", models.IntegerField(default=0, help_text="源石")),
                ("note", models.TextField(blank=True, verbose_name="备注")),
                (
                    "develop_resources",
                    models.ManyToManyField(
                        help_text="养成资源",
                        through="pack.DevelopList",
                        to="pack.developresource",
                    ),
                ),
                (
                    "gacha_resources",
                    models.ManyToManyField(
                        help_text="抽卡资源",
                        through="pack.GachaList",
                        to="pack.gacharesource",
                    ),
                ),
                (
                    "other_items",
                    models.ManyToManyField(
                        help_text="其它", through="pack.OtherList", to="pack.otheritem"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="otherlist",
            name="pack",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pack.pack"
            ),
        ),
        migrations.AddField(
            model_name="gachalist",
            name="gacha_resource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pack.gacharesource"
            ),
        ),
        migrations.AddField(
            model_name="gachalist",
            name="pack",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pack.pack"
            ),
        ),
        migrations.AddField(
            model_name="developlist",
            name="develop_resource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pack.developresource"
            ),
        ),
        migrations.AddField(
            model_name="developlist",
            name="pack",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pack.pack"
            ),
        ),
    ]

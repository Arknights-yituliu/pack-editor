from django.db import models


class GachaResource(models.Model):
    name = models.CharField(max_length=40, unique=True, help_text="名称")
    orundum = models.IntegerField(help_text="等价合成玉")

    def __str__(self):
        return self.name


class DevelopResource(models.Model):
    name = models.CharField(max_length=40, unique=True, help_text="名称")
    pinyin = models.CharField(max_length=40, help_text="拼音")
    value = models.FloatField(null=True, default=0, help_text="等效理智价值")

    def __str__(self):
        return self.name


class OtherItem(models.Model):
    name = models.CharField(max_length=40, unique=True, help_text="名称")
    originium = models.IntegerField(blank=True, help_text="等价源石（不填表示难以估计）")

    def __str__(self):
        return self.name


class Pack(models.Model):
    class Limitation(models.TextChoices):
        ONCE = "1", "once"
        MONTHLY = "m", "monthly"
        WEEKLY = "w", "weekly"
        YEAR = "y", "year"
        PERMANENT = "p", "permanent"
        LIMITED = "l", "limited"

    name = models.CharField(
        max_length=40,
        unique=True,
        help_text="名称",
    )
    pack_id = models.IntegerField(unique=True, help_text="礼包ID")
    limitation = models.CharField(
        max_length=1,
        choices=Limitation.choices,
        help_text="购买限制",
    )
    price = models.IntegerField(help_text="价格（元）")
    on_sale = models.BooleanField(default=True, help_text="是否在售")
    originium = models.IntegerField(default=0, help_text="源石")
    gacha_resources = models.ManyToManyField(
        GachaResource,
        help_text="抽卡资源",
        through="GachaList",
    )
    develop_resources = models.ManyToManyField(
        DevelopResource,
        help_text="养成资源",
        through="DevelopList",
    )
    other_items = models.ManyToManyField(
        OtherItem,
        help_text="其它",
        through="OtherList",
    )
    note = models.TextField("备注", blank=True)

    def __str__(self):
        return self.name


class GachaList(models.Model):
    gacha_resource = models.ForeignKey(GachaResource, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    count = models.IntegerField()


class DevelopList(models.Model):
    develop_resource = models.ForeignKey(DevelopResource, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    count = models.IntegerField()


class OtherList(models.Model):
    other_item = models.ForeignKey(OtherItem, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    count = models.IntegerField()

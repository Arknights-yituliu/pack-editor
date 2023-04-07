from django.db import models


class GachaResource(models.Model):
    """抽卡资源"""

    name = models.CharField(max_length=40, unique=True, help_text="名称")
    orundum = models.IntegerField(help_text="等价合成玉")

    def __str__(self):
        return self.name


class DevelopResource(models.Model):
    """养成资源"""

    name = models.CharField(max_length=40, unique=True, help_text="名称")
    pinyin = models.CharField(max_length=40, help_text="拼音")
    value = models.FloatField(null=True, default=0, help_text="等效理智价值")

    def __str__(self):
        return self.name


class OtherItem(models.Model):
    """其它资源"""

    name = models.CharField(max_length=40, unique=True, help_text="名称")
    originium = models.IntegerField(help_text="等价源石")

    def __str__(self):
        return self.name


class Pack(models.Model):
    """礼包"""

    class Limitation(models.TextChoices):
        ONCE = "1", "once"
        MONTHLY = "m", "monthly"
        WEEKLY = "w", "weekly"
        YEAR = "y", "year"
        PERMANENT = "p", "permanent"
        LIMITED = "l", "limited"

    class OnSaleControl(models.TextChoices):
        MANUAL_ON = "on", "在售（忽略时间）"
        MANUAL_OFF = "off", "停售（忽略时间）"
        BY_TIME = "time", "自动（时间控制）"

    name = models.CharField(
        max_length=40,
        unique=True,
        help_text="名称",
    )
    image = models.CharField(
        blank=True,
        max_length=40,
        help_text="图片名称（不填则使用名称）",
    )
    display_name = models.CharField(
        blank=True,
        max_length=40,
        help_text="显示名称（不填则使用名称）",
    )
    pack_id = models.IntegerField(unique=True, help_text="礼包ID")
    limitation = models.CharField(
        max_length=1,
        choices=Limitation.choices,
        help_text="购买限制",
    )
    price = models.IntegerField(help_text="价格（元）")
    on_sale_control = models.CharField(
        max_length=10,
        choices=OnSaleControl.choices,
        default=OnSaleControl.BY_TIME,
        help_text="若起始与结束日期均为空，则礼包永久在售",
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        help_text="开售日期，留空时不检查开售日期",
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="停售日期，留空时不检查停售日期",
    )
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

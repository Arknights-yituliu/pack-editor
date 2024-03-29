from django.contrib import admin
from .models import (
    Pack,
    GachaResource,
    DevelopResource,
    OtherItem,
    GachaList,
    DevelopList,
    OtherList,
)
from pypinyin import lazy_pinyin
import requests
from django_object_actions import DjangoObjectActions, action
import datetime
from django.utils.html import format_html


@admin.register(GachaResource)
class GachaAdmin(admin.ModelAdmin):
    pass


@admin.register(DevelopResource)
class DevelopAdmin(DjangoObjectActions, admin.ModelAdmin):
    ordering = ["pinyin"]
    search_fields = ["name"]
    fields = ("name", "value")
    changelist_actions = ("update_value",)
    list_display = ["name", "value", "in_pack"]

    def save_model(self, request, obj, form, change):
        if not obj.pinyin:
            obj.pinyin = "".join(lazy_pinyin(obj.name))
        super().save_model(request, obj, form, change)

    @action(label="更新等效理智")
    def update_value(modeladmin, request, queryset):
        r = requests.get(
            "https://backend.yituliu.site/item/value/",
            params={"expCoefficient": 0.625},
        )
        data = r.json()["data"]
        qs = DevelopResource.objects.all()
        for i in data:
            name = i["itemName"]
            qs.update_or_create(
                name=name,
                defaults={
                    "pinyin": "".join(lazy_pinyin(name)),
                    "value": i["itemValueAp"],
                },
            )

    @admin.display(description="礼包")
    def in_pack(self, obj):
        pack_list = [f"{p.pack.name}" for p in obj.developlist_set.all()]
        if (length := len(pack_list)) > 2:
            return f"{pack_list[0]}, {pack_list[1]} 等（共{length}个）"
        else:
            return ", ".join(pack_list)


@admin.register(OtherItem)
class OtherAdmin(admin.ModelAdmin):
    list_display = ["name", "originium"]


class GachaInline(admin.TabularInline):
    model = GachaList
    extra = 3


class DevelopInline(admin.TabularInline):
    model = DevelopList
    extra = 5
    autocomplete_fields = ["develop_resource"]


class OtherInline(admin.TabularInline):
    model = OtherList
    extra = 0


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    fields = (
        ("name", "pack_id"),
        "display_name",
        "image",
        "limitation",
        "price",
        ("on_sale_control", "start_date", "end_date"),
        "originium",
        "note",
        "img_preview",
        "img",
    )
    radio_fields = {"limitation": admin.HORIZONTAL}
    inlines = [GachaInline, DevelopInline, OtherInline]
    list_display = [
        "name",
        "list_img_preview",
        "pack_id",
        "limitation",
        "price",
        "originium",
        "on_sale",
        "date_range",
        "note",
    ]
    readonly_fields = [
        "img_preview",
    ]

    @admin.display(description="在售状态")
    def on_sale(self, obj):
        if (sale_control := obj.on_sale_control) == Pack.OnSaleControl.MANUAL_ON:
            return "在售（忽略时间）"
        elif sale_control == Pack.OnSaleControl.MANUAL_OFF:
            return "停售（忽略时间）"
        else:
            now = datetime.date.today()
            if obj.start_date and now < obj.start_date:
                return "未开售（时间控制）"
            elif obj.end_date and now > obj.end_date:
                return "已停售（时间控制）"
            else:
                return "在售（时间控制）"

    @admin.display(description="上架时间")
    def date_range(self, obj):
        if (sale_control := obj.on_sale_control) != Pack.OnSaleControl.BY_TIME:
            return "-"
        if obj.start_date and obj.end_date:
            return obj.start_date.isoformat() + "-" + obj.end_date.isoformat()
        elif obj.start_date:
            return obj.start_date.isoformat() + " - +∞"
        elif obj.end_date:
            return "-∞ - " + obj.end_date.isoformat()
        else:
            return "-∞ - +∞"

    @admin.display(description="礼包图片")
    def list_img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" height="16px" />', obj.img.url)
        else:
            return "无"

    @admin.display(description="礼包图片")
    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" />', obj.img.url)
        else:
            return "无"

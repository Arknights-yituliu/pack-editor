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


@admin.register(GachaResource)
class GachaAdmin(admin.ModelAdmin):
    pass


@admin.register(DevelopResource)
class DevelopAdmin(DjangoObjectActions, admin.ModelAdmin):
    ordering = ["pinyin"]
    search_fields = ["name"]
    fields = ("name",)
    changelist_actions = ("update_value",)
    list_display = ["name", "value"]

    def save_model(self, request, obj, form, change):
        if not obj.pinyin:
            obj.pinyin = "".join(lazy_pinyin(obj.name))
        super().save_model(request, obj, form, change)

    @action(label="更新等效理智")
    def update_value(modeladmin, request, queryset):
        r = requests.get(
            "https://backend.yituliu.site/api/find/item/value/",
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
                    "value": i["itemValue"],
                },
            )


@admin.register(OtherItem)
class OtherAdmin(admin.ModelAdmin):
    pass


class GachaInline(admin.TabularInline):
    model = GachaList
    extra = 3


class DevelopInline(admin.TabularInline):
    model = DevelopList
    extra = 5
    autocomplete_fields = ["develop_resource"]


class OtherInline(admin.StackedInline):
    model = OtherList
    extra = 0


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    fields = (
        ("name", "pack_id"),
        "limitation",
        ("price", "on_sale"),
        "originium",
        "note",
    )
    radio_fields = {"limitation": admin.HORIZONTAL}
    inlines = [GachaInline, DevelopInline, OtherInline]
    list_display = [
        "name",
        "pack_id",
        "limitation",
        "price",
        "originium",
        "on_sale",
        "note",
    ]

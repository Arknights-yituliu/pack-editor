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


@admin.register(GachaResource)
class GachaAdmin(admin.ModelAdmin):
    ordering = ["name"]


@admin.register(DevelopResource)
class DevelopAdmin(admin.ModelAdmin):
    ordering = ["name"]


@admin.register(OtherItem)
class OtherAdmin(admin.ModelAdmin):
    ordering = ["name"]


class GachaNestedInline(admin.TabularInline):
    model = GachaResource
    extra = 0


class GachaInline(admin.TabularInline):
    model = GachaList
    extra = 0


class DevelopInline(admin.TabularInline):
    model = DevelopList
    extra = 0


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

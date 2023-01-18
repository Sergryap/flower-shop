from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Bouquet, Category, Client, Order, Shop, Staff


@admin.display(description='Превью изображения')
def preview(model):
    if not model.image:
        return 'выберите картинку'
    return mark_safe(f'<img src="{model.image.url}" style="max-height: 200px;">')


class CategoryInline(admin.TabularInline):
    model = Category.bouquets.through
    extra = 1


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]

    fields = [
        'title',
        'price',
        preview,
        'image',
        'height',
        'width',
        'discription',
        'structure',
    ]

    list_display = [
        'title',
        'price',
        preview,
    ]

    readonly_fields = [
        preview,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


class BouquetInline(admin.TabularInline):
    can_delete = False
    model = Bouquet.orders.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [BouquetInline]
    exclude = [
        'bouquets'
    ]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    fields = [
        'phonenumber',
        'address',
        preview,
        'latitude',
        'longitude',
    ]

    list_display = [
        'phonenumber',
        'address',
        preview,
    ]

    readonly_fields = [
        preview,
    ]


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass

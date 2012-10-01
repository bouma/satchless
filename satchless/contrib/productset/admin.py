# -*- coding:utf-8 -*-
from django.contrib import admin
from satchless.contrib.productset.models import ProductSet, ProductSetItem, ProductSetImage
from products import widgets
import django.db.models


class ImageInline(admin.TabularInline):
    formfield_overrides = {
        django.db.models.ImageField: { 'widget': widgets.AdminImageWidget },
    }

class ProductSetImageInline(ImageInline):
    extra = 4
    max_num = 10
    model = ProductSetImage
    sortable_field_name = "sort"

class ProductSetAdmin(admin.ModelAdmin):
    inlines = [ProductSetImageInline]

class ProductSetItemAdmin(admin.ModelAdmin):
    pass

class ProductSetImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProductSet, ProductSetAdmin)
admin.site.register(ProductSetItem, ProductSetItemAdmin)
admin.site.register(ProductSetImage, ProductSetImageAdmin)
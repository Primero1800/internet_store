from django.contrib import admin
from django.utils.translation import gettext as _

from store.models import Brand, Image, Additional_information, Product, Rubric


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    list_display_links = ('title',)
    search_fields = ('title', 'description',)
    list_per_page = 30


admin.site.register(Brand, BrandAdmin)


class ImageInline(admin.TabularInline):
    model = Image


class AIInline(admin.TabularInline):
    model = Additional_information

    class Meta:
        verbose_name = _("Дополнительная информация")


class ProductInline(admin.StackedInline):
    model = Rubric.products.through


class RubricInline(admin.StackedInline):
    model = Product.rubrics.through


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('pk', 'title', 'price', 'quantity', 'is_on_sale', 'brand', 'published',)
    list_display_links = ('pk', 'title',)
    search_fields = ('pk', 'title', 'description',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 30
    inlines = [ImageInline, AIInline,]


admin.site.register(Product, ProductAdmin)


class RubricAdmin(admin.ModelAdmin):
    model = Rubric
    list_display = ('id', 'title', 'slug', 'image',)
    list_display_links = ('id', 'title', )
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductInline]


admin.site.register(Rubric, RubricAdmin)

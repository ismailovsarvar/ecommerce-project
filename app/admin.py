from django.contrib import admin
from import_export import resources

from app.models import Product, Image, Attribute, AttributeValue, ProductAttribute

# Register your models here.


# admin.site.register(Product)
# admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'rating', 'quantity']
    search_fields = ['name', 'price', 'quantity']
    list_filter = ['price', 'rating', 'quantity']


@admin.register(Image)
class ImagesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'product']
    search_fields = ['product']


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

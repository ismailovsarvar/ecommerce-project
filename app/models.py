from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=300, null=True)
    price = models.FloatField()
    rating = models.FloatField()
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def get_attributes(self) -> list[dict]:
        product_attributes = ProductAttribute.objects.filter(product=self)
        attributes = []
        for product_attributes in product_attributes:
            attributes.append({
                'attribute_key': product_attributes.attribute.key_name,
                'attribute_value': product_attributes.attribute_value.value_name
            })  # [{}, {}, {}]
        return attributes

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='products', null=True)
    product = models.ForeignKey('app.Product', on_delete=models.SET_NULL, related_name='images', null=True)

    def __str__(self):
        return self.image.name


class Attribute(models.Model):
    key_name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.key_name


class AttributeValue(models.Model):
    value_name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.value_name


class ProductAttribute(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('app.Attribute', on_delete=models.CASCADE)
    attribute_value = models.ForeignKey('app.AttributeValue', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

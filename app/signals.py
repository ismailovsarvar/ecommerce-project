from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from app.models import Product


@receiver(post_save, sender=Product)
def product_save(sender, instance, created, **kwargs):
    if created:
        print(f'Product {instance.name} created')
        print(kwargs)
    else:
        print(f'Product {instance.name} updated')


@receiver(pre_delete, sender=Product)
def product_delete(sender, instance, **kwargs):
    print(f'Product {instance.name} deleted')

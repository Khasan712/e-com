from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Category, Product, ProductItem


@receiver(post_save, sender=Category)
def category_save_and_edit_signals(sender, instance, created, **kwargs):
    if created or instance.is_deleted or not instance.is_active:
        cache.delete('all_categories')


@receiver(post_save, sender=Product)
def product_signals(sender, instance, created, **kwargs):
    cache.delete('all_categories')
    if not instance.is_active and instance.is_deleted:
        instance.product_card.update(is_active=False, is_deleted=True)


@receiver(post_save, sender=ProductItem)
def product_item_signals(sender, instance, created, **kwargs):
    cache.delete('all_categories')

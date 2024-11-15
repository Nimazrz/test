from django.db.models.signals import pre_save
from django.dispatch import receiver
from.models import Product
from decimal import Decimal

@receiver(pre_save, sender=Product)
def calculate_new_price(sender, instance, **kwargs):
    instance.new_price = Decimal(instance.price) * (100 - instance.offer) / 100

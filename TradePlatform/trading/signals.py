from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from trading import models


@receiver(post_save, sender=models.Trade)
def check_price(sender, instance, **kwargs):
    price = instance.unit_price
    item = instance.item
    date = timezone.now()
    exists = models.Price.objects.filter(item=item).first()
    if exists:
        if exists.price > price:
            exists.price = price
            exists.date = date
            exists.save(update_fields=['price', 'date'])
    else:
        price = models.Price(item=item,
                             date=date,
                             price=price)
        price.save()

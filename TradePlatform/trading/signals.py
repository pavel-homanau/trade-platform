from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from trading.models import Price, Trade


@receiver(post_save, sender=Trade)
def check_price(sender, instance, **kwargs):
    """Changes price, while created a trade."""
    price = instance.unit_price
    item = instance.item
    date = timezone.now()
    exists = Price.objects.filter(item=item).first()
    if exists:
        if exists.price > price:
            exists.price = price
            exists.date = date
            exists.save(update_fields=['price', 'date'])
    else:
        price = Price(item=item, date=date, price=price)
        price.save()

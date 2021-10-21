from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Currency(models.Model):
    name = models.CharField("Name", max_length=128, unique=True)


class Item(models.Model):
    name = models.CharField("Name", max_length=128, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True,
                                null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    details = models.TextField("Details", blank=True, null=True,
                               max_length=512)


class Price(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='prices',
                             related_query_name='prices')
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                blank=True, null=True)
    date = models.DateTimeField(unique=True, blank=True, null=True)


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField("Stock quantity", default=0)


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Offer(models.Model):
    order_type_choice = (
        (1, 'buy'),
        (2, 'sell'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order_type = models.PositiveSmallIntegerField(choices=order_type_choice)
    entry_quantity = models.IntegerField("Requested quantity",
                                         blank=True,
                                         null=True)
    current_quantity = models.IntegerField("Current quantity",
                                           blank=True,
                                           null=True)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2,
                                blank=True,
                                null=True)
    is_active = models.BooleanField(default=True)


class Trade(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='seller_trade',
                               related_query_name='seller_trade',
                               )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='buyer_trade',
                              related_query_name='buyer_trade',
                              )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    buyer_offer = models.ForeignKey(Offer, on_delete=models.CASCADE,
                                    related_name='buyer_trade',
                                    related_query_name='buyer_trade',
                                    )
    seller_offer = models.ForeignKey(Offer, on_delete=models.CASCADE,
                                     related_name='seller_trade',
                                     related_query_name='seller_trade',
                                     )

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import Service

from trading.models import (Item, Inventory, Offer,
                            Trade)


class CreateTrade(Service):

    def process(self):
        """Creates a trade from offers."""
        active_offers = Offer.objects.filter(is_active=True). \
            select_related('item', 'user'). \
            only('item__price', 'user__cash',
                 'order_type', 'entry_quantity', 'price')
        buy_offers = active_offers.filter(order_type=1)

        for buy_offer in buy_offers:
            item = buy_offer.item
            sell_offers = active_offers.filter(order_type=2). \
                filter(item=item, price__gte=buy_offer.price). \
                order_by('price')

            for sell_offer in sell_offers:
                seller = sell_offer.user
                buyer = buy_offer.user

                trade_object = Trade(item=item,
                                     buyer=buyer,
                                     seller=seller,
                                     quantity=min(sell_offer.
                                                  entry_quantity,
                                                  buy_offer.
                                                  entry_quantity),
                                     unit_price=sell_offer.price,
                                     buyer_offer=buy_offer,
                                     seller_offer=sell_offer)

                total_price = trade_object.unit_price * trade_object.quantity
                if (buyer.cash - total_price) >= 0:
                    trade_object.save()

                    seller.cash += total_price
                    seller.save(update_fields=['cash'])

                    buyer.cash -= total_price
                    buyer.save(update_fields=['cash'])

                    item_in_buyer_inv = Inventory.objects. \
                        filter(user=buyer, item=item).first()
                    item_in_seller_inv = Inventory.objects. \
                        get(user=seller, item=item)

                    if item_in_buyer_inv:
                        item_in_buyer_inv.quantity += trade_object.quantity
                        item_in_buyer_inv.save(update_fields=['quantity'])
                    else:
                        item_in_buyer_inv = Inventory(item=buy_offer.item,
                                                      user=buyer,
                                                      quantity=trade_object.
                                                      quantity)
                        item_in_buyer_inv.save()

                    item_in_seller_inv.quantity -= trade_object.quantity
                    if item_in_seller_inv.quantity == 0:
                        item_in_seller_inv.delete()
                    else:
                        item_in_seller_inv.save(update_fields=['quantity'])

                    buy_offer.entry_quantity -= trade_object.quantity
                    if buy_offer.entry_quantity == 0:
                        buy_offer.is_active = False
                        buy_offer.save(update_fields=['is_active'])
                    else:
                        buy_offer.save(update_fields=['entry_quantity'])

                    sell_offer.entry_quantity -= trade_object.quantity
                    if sell_offer.entry_quantity == 0:
                        sell_offer.is_active = False
                        sell_offer.save(update_fields=['is_active'])
                    else:
                        sell_offer.save(update_fields=['entry_quantity'])


class CheckPrice(Service):

    def process(self):
        """Checks price of item."""
        user = get_user_model().objects.get(id=self.data['serializer']['user'])
        item = Item.objects.get(id=self.data['serializer']['item'])
        entry_quantity = self.data['serializer']['entry_quantity']
        try:
            item_in_inventory = Inventory.objects. \
                get(user=user,
                    item=item)
            item_in_inventory.quantity += entry_quantity
            item_in_inventory.save()
        except ObjectDoesNotExist:
            item_in_inventory = Inventory(item=item,
                                          user=user,
                                          quantity=entry_quantity)
            item_in_inventory.save()

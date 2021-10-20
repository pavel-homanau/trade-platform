from service_objects.services import Service
from trading import models


class CreateTrade(Service):

    def process(self):
        active_offers = models.Offer.objects.filter(is_active=True). \
            select_related('item', 'user').\
            only('item__price', 'user__cash',
                 'order_type', 'entry_quantity', 'price')
        buy_offers = active_offers.filter(order_type=1)

        for buy_offer in buy_offers:
            item = buy_offer.item
            sell_offers = active_offers.filter(order_type=2).\
                filter(item=item, price__gte=buy_offer.price).\
                order_by('price')

            for sell_offer in sell_offers:
                seller = sell_offer.user
                buyer = buy_offer.user

                trade_object = models.Trade(item=item,
                                            buyer=buyer,
                                            seller=seller,
                                            quantity=min(sell_offer.entry_quantity,
                                                         buy_offer.entry_quantity),
                                            unit_price=sell_offer.price,
                                            buyer_offer=buy_offer,
                                            seller_offer=sell_offer)

                if (buyer.cash - trade_object.unit_price * trade_object.quantity) >= 0:
                    trade_object.save()

                    seller.cash += trade_object.unit_price * trade_object.quantity
                    seller.save(update_fields=['cash'])

                    buyer.cash -= trade_object.unit_price * trade_object.quantity
                    buyer.save(update_fields=['cash'])

                    item_in_buyer_inventory = models.Inventory.objects.filter(user=buyer,
                                                                              item=item).first()
                    item_in_seller_inventory = models.Inventory.objects.get(user=seller,
                                                                            item=item)

                    if item_in_buyer_inventory:
                        item_in_buyer_inventory.quantity += trade_object.quantity
                        item_in_buyer_inventory.save(update_fields=['quantity'])
                    else:
                        item_in_buyer_inventory = models.Inventory(item=buy_offer.item,
                                                                   user=buyer,
                                                                   quantity=trade_object.quantity)
                        item_in_buyer_inventory.save()

                    item_in_seller_inventory.quantity -= trade_object.quantity
                    if item_in_seller_inventory.quantity == 0:
                        item_in_seller_inventory.delete()
                    else:
                        item_in_seller_inventory.save(update_fields=['quantity'])

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

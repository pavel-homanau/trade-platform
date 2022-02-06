import os
from json import dumps

from kafka import KafkaProducer
from service_objects.services import Service

from trading import models


class CreateTrade(Service):
    """Create trade from offers."""

    trade_object = None

    def quantity_process(self):
        """Update quantity if trade object. If no quantity -
        change active status of offer to false."""

        buy_offer = self.trade_object.buyer_offer
        buy_offer.entry_quantity -= self.trade_object.quantity

        sell_offer = self.trade_object.seller_offer
        sell_offer.entry_quantity -= self.trade_object.quantity

        if buy_offer.entry_quantity == 0:
            buy_offer.is_active = False
        buy_offer.save(update_fields=['is_active', 'entry_quantity'])

        if sell_offer.entry_quantity == 0:
            sell_offer.is_active = False
        sell_offer.save(update_fields=['is_active', 'entry_quantity'])

    def inventory_process(self):
        """Update inventory data."""

        buyer = self.trade_object.buyer
        seller = self.trade_object.buyer
        item = self.trade_object.item
        item_in_buyer_inventory = models.Inventory.\
            objects.filter(user=buyer, item=item).first()
        item_in_seller_inventory = models.Inventory.\
            objects.get(user=seller, item=item)

        if item_in_buyer_inventory:
            item_in_buyer_inventory.quantity += self.trade_object.quantity
        else:
            item_in_buyer_inventory = models.Inventory(
                item=self.trade_object.buy_offer.item,
                user=buyer,
                quantity=self.trade_object.trade_object.quantity
            )
        item_in_buyer_inventory.save()

        item_in_seller_inventory.quantity -= self.trade_object.quantity
        if item_in_seller_inventory.quantity == 0:
            item_in_seller_inventory.delete()
        else:
            item_in_seller_inventory.save(update_fields=['quantity'])

    def send_emails(self):
        """ Send to microservice emails and item of trading."""

        # emails_dict = {
        #     'seller_email': self.trade_object.seller.email,
        #     'buyer_email': self.trade_object.buyer.email,
        #     'item': self.trade_object.item
        # }

        def_emails_dict = {
            'seller_email': os.environ.get("TEST_EMAIL_ADDR"),
            'buyer_email': os.environ.get("TEST_EMAIL_ADDR"),
            'item': 'test item'
        }

        print('[*]Start send email.')
        email_producer = KafkaProducer(
            bootstrap_servers=os.environ.get("BOOTSTRAP_SERVER"),
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )

        email_producer.send(os.environ.get("EMAIL_TOPIC"), value=def_emails_dict)
        print('[*]End of celery email.')

    def process(self):
        """Create process."""

        active_offers = models.Offer.objects.filter(is_active=True).\
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

                trade_object = models.Trade(
                    item=item,
                    buyer=buy_offer.user,
                    seller=sell_offer.user,
                    quantity=min(sell_offer.entry_quantity,
                                 buy_offer.entry_quantity),
                    unit_price=sell_offer.price,
                    buyer_offer=buy_offer,
                    seller_offer=sell_offer
                )

                if (buyer.cash - trade_object.unit_price * trade_object.quantity) >= 0:
                    trade_object.save()

                    seller.cash += trade_object.unit_price * trade_object.quantity
                    seller.save(update_fields=['cash'])

                    buyer.cash -= trade_object.unit_price * trade_object.quantity
                    buyer.save(update_fields=['cash'])

                    self.inventory_process()
                    self.quantity_process()
                    self.send_emails()


class SendEmail(Service):
    def process(self):
        CreateTrade().send_emails()

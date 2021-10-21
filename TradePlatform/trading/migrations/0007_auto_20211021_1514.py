# Generated by Django 3.2.8 on 2021-10-21 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trading', '0006_remove_price_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trading.item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inventory',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trading.currency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trading.item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='price',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='prices', related_query_name='prices', to='trading.item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trade',
            name='buyer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_trade', related_query_name='buyer_trade', to='authentication.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trade',
            name='buyer_offer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_trade', related_query_name='buyer_trade', to='trading.offer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trade',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trading.item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trade',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='seller_trade', related_query_name='seller_trade', to='authentication.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trade',
            name='seller_offer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='seller_trade', related_query_name='seller_trade', to='trading.offer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trading.item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
            preserve_default=False,
        ),
    ]

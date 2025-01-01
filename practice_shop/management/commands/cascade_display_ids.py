from django.core.management.base import BaseCommand
from django.db import transaction
from practice_shop.models import Order

class Command(BaseCommand):
    help = 'Cascades the display_id of orders sequentially.'

    def handle(self, *args, **kwargs):
        orders = Order.objects.order_by('created_at')  # You can also use 'id' to order by primary key
        base_display_id = 1

        with transaction.atomic():
            for order in orders:
                order.display_id = base_display_id
                order.save(update_fields=['display_id'])
                base_display_id += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated display_id for {len(orders)} orders.'))

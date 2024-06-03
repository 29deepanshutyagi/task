# api/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor
from django.db.models import F
from datetime import timedelta

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    purchase_orders = vendor.purchase_orders.filter(status='completed')

    if purchase_orders.exists():
        # On-Time Delivery Rate
        on_time_count = purchase_orders.filter(delivery_date__lte=F('delivery_date')).count()
        vendor.on_time_delivery_rate = on_time_count / purchase_orders.count()

        # Quality Rating Average
        quality_ratings = purchase_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

        # Average Response Time
        response_times = [po.acknowledgment_date - po.issue_date for po in purchase_orders if po.acknowledgment_date]
        vendor.average_response_time = sum(response_times, timedelta()) / len(response_times) if response_times else 0

        # Fulfillment Rate
        fulfilled_count = purchase_orders.filter(status='completed', quality_rating__isnull=False).count()
        vendor.fulfillment_rate = fulfilled_count / purchase_orders.count()

        vendor.save()

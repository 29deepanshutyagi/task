# api/views.py

from rest_framework import viewsets
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder, Vendor
from django.utils import timezone


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class VendorPerformanceView(APIView):
    def get(self, request, vendor_id, format=None):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            data = {
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
class AcknowledgePOView(APIView):
    def post(self, request, po_id, format=None):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Update Vendor Metrics
            vendor = purchase_order.vendor
            purchase_orders = vendor.purchase_orders.filter(status='completed')

            if purchase_orders.exists():
                # Average Response Time
                response_times = [po.acknowledgment_date - po.issue_date for po in purchase_orders if po.acknowledgment_date]
                vendor.average_response_time = sum(response_times, timedelta()) / len(response_times) if response_times else 0
                vendor.save()

            return Response(status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
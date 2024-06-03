# api/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder

class VendorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="TEST123"
        )

    def test_create_vendor(self):
        response = self.client.post('/api/vendors/', {
            'name': 'New Vendor',
            'contact_details': 'New Contact',
            'address': 'New Address',
            'vendor_code': 'NEW123'
        }, format='json')
        self.assertEqual(response.status_code, 201)

class PurchaseOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="TEST123"
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=self.vendor,
            order_date="2024-01-01T00:00:00Z",
            delivery_date="2024-01-10T00:00:00Z",
            items={},
            quantity=10,
            status="pending",
            issue_date="2024-01-01T00:00:00Z"
        )

    def test_create_purchase_order(self):
        response = self.client.post('/api/purchase_orders/', {
            'po_number': 'PO124',
            'vendor': self.vendor.id,
            'order_date': '2024-01-02T00:00:00Z',
            'delivery_date': '2024-01-12T00:00:00Z',
            'items': {},
            'quantity': 5,
            'status': 'pending',
            'issue_date': '2024-01-02T00:00:00Z'
        }, format='json')
        self.assertEqual(response.status_code, 201)

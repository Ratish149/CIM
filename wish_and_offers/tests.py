from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Offer, Wish


class DataConversionTests(APITestCase):
    def setUp(self):
        self.url = reverse("data-conversion")
        self.wish = Wish.objects.create(
            full_name="Test Wisher",
            mobile_no="1234567890",
            email="wisher@test.com",
            company_name="Test Co",
            address="Test Addr",
            title="Test Wish Title",
            type="Product",
        )
        self.offer = Offer.objects.create(
            full_name="Test Offerer",
            mobile_no="0987654321",
            email="offerer@test.com",
            company_name="Offer Co",
            address="Offer Addr",
            title="Test Offer Title",
            type="Product",
        )

    def test_wish_to_offer_conversion(self):
        data = {
            "source_type": "wish",
            "source_id": self.wish.id,
            "target_type": "offer",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.wish.title)
        self.assertFalse(Wish.objects.filter(id=self.wish.id).exists())
        self.assertTrue(Offer.objects.filter(id=response.data["id"]).exists())

    def test_offer_to_wish_conversion(self):
        data = {
            "source_type": "offer",
            "source_id": self.offer.id,
            "target_type": "wish",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.offer.title)
        self.assertFalse(Offer.objects.filter(id=self.offer.id).exists())
        self.assertTrue(Wish.objects.filter(id=response.data["id"]).exists())

    def test_invalid_conversion_same_type(self):
        data = {
            "source_type": "wish",
            "source_id": self.wish.id,
            "target_type": "wish",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wish_not_found(self):
        data = {
            "source_type": "wish",
            "source_id": 9999,
            "target_type": "offer",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

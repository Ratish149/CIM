import os

import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIM.settings")
django.setup()

from django.urls import reverse
from rest_framework.test import APIClient

from wish_and_offers.models import Offer, Wish


def verify_conversion():
    client = APIClient()
    url = reverse("data-conversion")

    # 1. Test Wish -> Offer
    print("Testing Wish -> Offer conversion...")
    wish = Wish.objects.create(
        full_name="Test Wisher",
        mobile_no="1234567890",
        email="wisher@test.com",
        company_name="Test Co",
        address="Test Addr",
        title="Test Wish Title",
        type="Product",
    )
    wish_id = wish.id

    response = client.post(
        url,
        {"source_type": "wish", "source_id": wish_id, "target_type": "offer"},
        format="json",
    )

    if response.status_code == 201:
        print("Success: Wish converted to Offer.")
        offer_id = response.data["id"]
        if (
            not Wish.objects.filter(id=wish_id).exists()
            and Offer.objects.filter(id=offer_id).exists()
        ):
            print("Verified: Wish deleted, Offer created.")
            new_offer = Offer.objects.get(id=offer_id)
            if new_offer.title == "Test Wish Title":
                print("Verified: Data copied correctly.")
            else:
                print(
                    f"Error: Data mismatch. Expected 'Test Wish Title', got '{new_offer.title}'"
                )
        else:
            print("Error: Wish still exists or Offer not found.")
    else:
        print(f"Error: Conversion failed with status {response.status_code}")
        print(response.data)

    # 2. Test Offer -> Wish
    print("\nTesting Offer -> Wish conversion...")
    offer = Offer.objects.create(
        full_name="Test Offerer",
        mobile_no="0987654321",
        email="offerer@test.com",
        company_name="Offer Co",
        address="Offer Addr",
        title="Test Offer Title",
        type="Product",
    )
    offer_id = offer.id

    response = client.post(
        url,
        {"source_type": "offer", "source_id": offer_id, "target_type": "wish"},
        format="json",
    )

    if response.status_code == 201:
        print("Success: Offer converted to Wish.")
        new_wish_id = response.data["id"]
        if (
            not Offer.objects.filter(id=offer_id).exists()
            and Wish.objects.filter(id=new_wish_id).exists()
        ):
            print("Verified: Offer deleted, Wish created.")
            new_wish = Wish.objects.get(id=new_wish_id)
            if new_wish.title == "Test Offer Title":
                print("Verified: Data copied correctly.")
            else:
                print(
                    f"Error: Data mismatch. Expected 'Test Offer Title', got '{new_wish.title}'"
                )
        else:
            print("Error: Offer still exists or Wish not found.")
    else:
        print(f"Error: Conversion failed with status {response.status_code}")
        print(response.data)


if __name__ == "__main__":
    verify_conversion()

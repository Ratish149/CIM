import os

import django
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIM.settings")
django.setup()

from wish_and_offers.models import Wish


def recalculate_all_matches():
    print("Starting match recalculation...")

    wishes = Wish.objects.all()
    print(f"Found {wishes.count()} wishes.")

    for wish in wishes:
        print(f"Recalculating matches for Wish: {wish.title} (ID: {wish.id})")
        wish.update_match_percentages()

    print("\nRecalculation complete.")


if __name__ == "__main__":
    recalculate_all_matches()

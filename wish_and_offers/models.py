from django.db import models
from difflib import SequenceMatcher
from accounts.models import CustomUser, Organization
from events.models import Event

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.FileField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    hs_code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    image = models.FileField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.hs_code})"

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to='service_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Wish(models.Model):
    WISH_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    WISH_TYPE = [
        ('Product', 'Product'),
        ('Service', 'Service'),
    ]

    title=models.CharField(max_length=200,default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='wishes', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishes', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='wishes', blank=True, null=True)
    status = models.CharField(max_length=10, choices=WISH_STATUS, default='Pending')
    wish_type = models.CharField(max_length=10, choices=WISH_TYPE, default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wish by {self.user.username} for {self.event.title if self.event else 'No Event'}"

class Offer(models.Model):
    OFFER_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    OFFER_TYPE = [
        ('Product', 'Product'),
        ('Service', 'Service'),
    ]
    title=models.CharField(max_length=200,default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='offers', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    status = models.CharField(max_length=10, choices=OFFER_STATUS, default='Pending')
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE, default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer by {self.user.username} for {self.event.title if self.event else 'No Event'}"

class Match(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, related_name='matches')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='matches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Match: {self.wish.user.username} with {self.offer.user.username}"

    @staticmethod
    def are_titles_similar(title1, title2, threshold=0.6):
        return SequenceMatcher(None, title1.lower(), title2.lower()).ratio() > threshold
    
    @staticmethod
    def calculate_match_score(wish, offer):
        score = 0
        max_score = 0
        weights = {
            'exact_match': 50,
            'category_match': 30,
            'title_similarity': 20
        }

        # Check for exact product/service match
        if (wish.product and offer.product and wish.product == offer.product) or \
           (wish.service and offer.service and wish.service == offer.service):
            score += weights['exact_match']
        # Check for category match
        elif (wish.product and offer.product and wish.product.category and offer.product.category and 
              wish.product.category == offer.product.category) or \
             (wish.service and offer.service and wish.service.category and offer.service.category and 
              wish.service.category == offer.service.category):
            score += weights['category_match']

        max_score += max(weights['exact_match'], weights['category_match'])

        # Check title similarity
        title_similarity = SequenceMatcher(None, wish.title.lower(), offer.title.lower()).ratio()
        score += weights['title_similarity'] * title_similarity
        max_score += weights['title_similarity']

        # Calculate percentage
        percentage_score = (score / max_score) * 100

        return round(percentage_score, 2)

    @classmethod
    def find_matches(cls):
        matches = []
        wishes = Wish.objects.filter(status='Pending')
        offers = Offer.objects.filter(status='Pending')

        for wish in wishes:
            for offer in offers:
                if wish.wish_type == offer.offer_type:
                    score = cls.calculate_match_score(wish, offer)
                    if score > 0:
                        match = cls(wish=wish, offer=offer)
                        matches.append((match, score))
        
        # Sort matches by score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    @classmethod
    def find_matches_for_wish(cls, wish_id):
        matches = []
        wish = Wish.objects.get(id=wish_id, status='Pending')
        offers = Offer.objects.filter(status='Pending')

        for offer in offers:
            if wish.wish_type == offer.offer_type:
                score = cls.calculate_match_score(wish, offer)
                if score > 0:
                    match = cls(wish=wish, offer=offer)
                    matches.append((match, score))
        
        # Sort matches by score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    @classmethod
    def find_matches_for_offer(cls, offer_id):
        matches = []
        offer = Offer.objects.get(id=offer_id, status='Pending')
        wishes = Wish.objects.filter(status='Pending')

        for wish in wishes:
            if wish.wish_type == offer.offer_type:
                score = cls.calculate_match_score(wish, offer)
                if score > 0:
                    match = cls(wish=wish, offer=offer)
                    matches.append((match, score))
        
        # Sort matches by score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

   
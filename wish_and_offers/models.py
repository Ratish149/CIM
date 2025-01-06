from django.db import models
from difflib import SequenceMatcher
from accounts.models import CustomUser, Organization
from events.models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class Detail(models.Model):
    DESIGNATION_CHOICES = [
        ('CEO', 'Chief Executive Officer'),
        ('CFO', 'Chief Financial Officer'),
        ('CTO', 'Chief Technology Officer'),
        ('CMO', 'Chief Marketing Officer'),
        ('COO', 'Chief Operating Officer'),
        ('CIO', 'Chief Information Officer'),
        ('CSO', 'Chief Security Officer'),
        ('Other', 'Other'),
    ]
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES)
    mobile_no = models.CharField(max_length=15)
    alternate_no = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=100, default='Nepal', null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    municipality = models.CharField(max_length=100, null=True, blank=True)
    ward = models.CharField(max_length=100, null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)
    image = models.FileField(upload_to='wish_and_offers/images', null=True, blank=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='service_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class HSCode(models.Model):
    hs_code = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.hs_code} - {self.description[:50]}"

class Wish(Detail):
    WISH_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200, default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='wishes', null=True, blank=True)
    product = models.ForeignKey(HSCode, on_delete=models.CASCADE, related_name='wishes', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_wishes', blank=True, null=True)
    status = models.CharField(max_length=10, choices=WISH_STATUS, default='Pending')
    type = models.CharField(max_length=10, choices=[('Product', 'Product'), ('Service', 'Service')], default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match_percentage = models.IntegerField(default=0)

    # Recursion guard for save
    _updating = False

    def save(self, *args, **kwargs):
        if not self._updating:
            try:
                self._updating = True
                super().save(*args, **kwargs)
                self.update_match_percentages()
            finally:
                self._updating = False
        else:
            super().save(*args, **kwargs)

    def update_match_percentages(self):
        matches = Match.find_matches_for_wish(self.id)
        created_matches = []
        for match, score in matches:
            if score > 80:
                match_obj, created = Match.objects.update_or_create(
                    wish=self, offer=match.offer, defaults={'match_percentage': score}
                )
                if created:
                    created_matches.append(match_obj)
                match.offer.match_percentage = score
                match.offer.save(update_fields=['match_percentage'])
        self.match_percentage = max([score for _, score in matches], default=0)
        self.save(update_fields=['match_percentage'])
        if created_matches:
            self.send_match_email(created_matches)

    def update_related_offer_matches(self):
        related_offers = Offer.objects.filter(status='Pending', type=self.type)
        for offer in related_offers:
            offer.update_match_percentages()

    def send_match_email(self, matches):
        subject = "Your Wish has New Matches!"
        html_message = render_to_string(
            'email_templates/match_notification.html', {'matches': matches, 'entity': self}
        )
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.email] + [match.offer.email for match in matches]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

class Offer(Detail):
    OFFER_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200, default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='offers', null=True, blank=True)
    product = models.ForeignKey(HSCode, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    status = models.CharField(max_length=10, choices=OFFER_STATUS, default='Pending')
    type = models.CharField(max_length=10, choices=[('Product', 'Product'), ('Service', 'Service')], default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match_percentage = models.IntegerField(default=0)

    # Recursion guard for save
    _updating = False

    def save(self, *args, **kwargs):
        if not self._updating:
            try:
                self._updating = True
                super().save(*args, **kwargs)
                self.update_match_percentages()
            finally:
                self._updating = False
        else:
            super().save(*args, **kwargs)

    def update_match_percentages(self):
        matches = Match.find_matches_for_offer(self.id)
        created_matches = []
        for match, score in matches:
            if score > 80:
                match_obj, created = Match.objects.update_or_create(
                    wish=match.wish, offer=self, defaults={'match_percentage': score}
                )
                if created:
                    created_matches.append(match_obj)
                match.wish.match_percentage = score
                match.wish.save(update_fields=['match_percentage'])
        self.match_percentage = max([score for _, score in matches], default=0)
        self.save(update_fields=['match_percentage'])
        if created_matches:
            self.send_match_email(created_matches)


    def send_match_email(self, matches):
        subject = "Your Offer has New Matches!"
        html_message = render_to_string(
            'email_templates/match_notification.html', {'matches': matches, 'entity': self}
        )
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.email] + [match.wish.email for match in matches]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

class Match(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, related_name='matches')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='matches')
    match_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def calculate_match_score(wish, offer):
        score = 0
        weights = {
            'product_match': 50,
            'service_match': 50,
            'title_similarity': 30,
        }

        # Product match
        if wish.product and offer.product and wish.product == offer.product:
            score += weights['product_match']

        # Service match
        if wish.service and offer.service and wish.service == offer.service:
            score += weights['service_match']

        # Title similarity
        title_similarity = SequenceMatcher(None, wish.title.lower(), offer.title.lower()).ratio() * 100
        score += min(title_similarity / 100 * weights['title_similarity'], weights['title_similarity'])

        return int(score)

    @classmethod
    def find_matches_for_wish(cls, wish_id):
        wish = Wish.objects.get(id=wish_id)
        offers = Offer.objects.filter(status='Pending', type=wish.type)
        matches = []
        for offer in offers:
            score = cls.calculate_match_score(wish, offer)
            matches.append((offer, score))
            
            if score > offer.match_percentage:
                offer.match_percentage = score
                offer.save(update_fields=['match_percentage'])  # Save the updated match_percentage

        return matches

    @classmethod
    def find_matches_for_offer(cls, offer_id):
        offer = Offer.objects.get(id=offer_id)
        wishes = Wish.objects.filter(status='Pending', type=offer.type)
        matches = []
        for wish in wishes:
            score = cls.calculate_match_score(wish, offer)
            matches.append((wish, score))

            if score > wish.match_percentage:
                wish.match_percentage = score
                wish.save(update_fields=['match_percentage'])  # Save the updated match_percentage

        return matches
    
    @classmethod
    def find_matches(cls):
        matches = []
        wishes = Wish.objects.filter(status='Pending')
        offers = Offer.objects.filter(status='Pending')
        for wish in wishes:
            for offer in offers:
                if wish.type == offer.type:
                    score = cls.calculate_match_score(wish, offer)
                    matches.append((wish, offer, score))
        return matches

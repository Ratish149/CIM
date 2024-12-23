from django.db import models
from difflib import SequenceMatcher
from accounts.models import CustomUser, Organization
from events.models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.mail import send_mail  # Import send_mail for sending emails
from django.template.loader import render_to_string  # Import for rendering email templates
from django.utils.html import strip_tags  # Import for stripping HTML tags

# Global flag to prevent recursion
is_handling_signal = False
is_handling_wish_signal = False

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
    description = models.TextField()
    image = models.FileField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    hs_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
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

class Wish(Detail):
    WISH_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    WISH_TYPE = [
        ('Product', 'Product'),
        ('Service', 'Service'),
    ]

    title = models.CharField(max_length=200, default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='wishes', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishes', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_wishes', blank=True, null=True)
    status = models.CharField(max_length=10, choices=WISH_STATUS, default='Pending')
    wish_type = models.CharField(max_length=10, choices=WISH_TYPE, default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match_percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} for {self.event.title if self.event else 'No Event'}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the original save method
        self.update_match_percentages()  # Update match percentages for all offers
        self.update_highest_match_percentage()  # Check and update highest match percentage for all wishes

    def update_match_percentages(self):
        matches = Match.find_matches_for_wish(self.id)
        highest_score = 0
        for match, score in matches:
            if score > highest_score:
                highest_score = score
            if score > 80:  # Save match if score is greater than 80%
                Match.objects.create(wish=self, offer=match.offer, match_percentage=score)
                self.send_match_email(self, match.offer)  # Send email notification

                # Update the offer's match_percentage if the score is greater
                if score > match.offer.match_percentage:
                    match.offer.match_percentage = score
                    match.offer.save(update_fields=['match_percentage'])  # Save the updated match_percentage for the offer

        if highest_score > 80:  # Update match percentage in Wish
            self.match_percentage = highest_score
            super().save(update_fields=['match_percentage'])  # Save only the match_percentage field

            # Update the offer's match_percentage if the highest score is greater
            for match, score in matches:
                if score == highest_score:
                    match.offer.match_percentage = highest_score
                    match.offer.save(update_fields=['match_percentage'])  # Save the updated match_percentage for the offer

    def update_highest_match_percentage(self):
        # Check for all offers to see if any has a higher match percentage
        offers = Offer.objects.filter(status='Pending')
        for offer in offers:
            score = Match.calculate_match_score(self, offer)
            if score > self.match_percentage:
                self.match_percentage = score
                self.save(update_fields=['match_percentage'])  # Update the match_percentage field
                
                # Update the offer's match_percentage if the score is greater
                if score > offer.match_percentage:
                    offer.match_percentage = score
                    offer.save(update_fields=['match_percentage'])  # Save the updated match_percentage for the offer

    def send_match_email(self, wish, offer):
        subject = "Your Wish has been Matched!"
        html_message = render_to_string('email_templates/match_notification.html', {'wish': wish, 'offer': offer})
        plain_message = strip_tags(html_message)
        from_email = 'your_email@example.com'  # Replace with your email
        recipient_list = [wish.email, offer.email]  # Assuming both Wish and Offer have an email field

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

class Offer(Detail):
    OFFER_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    OFFER_TYPE = [
        ('Product', 'Product'),
        ('Service', 'Service'),
    ]
    title = models.CharField(max_length=200, default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='offers', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    status = models.CharField(max_length=10, choices=OFFER_STATUS, default='Pending')
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE, default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match_percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} for {self.event.title if self.event else 'No Event'}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the original save method
        self.update_match_percentages()  # Update match percentages for all wishes
        self.update_highest_match_percentage()  # Check and update highest match percentage for all offers

    def update_match_percentages(self):
        matches = Match.find_matches_for_offer(self.id)
        highest_score = 0
        for match, score in matches:
            if score > highest_score:
                highest_score = score
            if score > 80:  # Save match if score is greater than 80%
                Match.objects.create(wish=match.wish, offer=self, match_percentage=score)
                self.send_match_email(match.wish, self)  # Send email notification

                # Update the wish's match_percentage if the score is greater
                if score > match.wish.match_percentage:
                    match.wish.match_percentage = score
                    match.wish.save(update_fields=['match_percentage'])  # Save the updated match_percentage for the wish

        if highest_score > 80:  # Update match percentage in Offer
            self.match_percentage = highest_score
            super().save(update_fields=['match_percentage'])  # Save only the match_percentage field

            # Update the wish's match_percentage if the highest score is greater
            for match, score in matches:
                if score == highest_score:
                    match.wish.match_percentage = highest_score
                    match.wish.save(update_fields=['match_percentage'])  # Save the updated match_percentage for the wish

    def update_highest_match_percentage(self):
        # Check for all wishes to see if any has a higher match percentage
        wishes = Wish.objects.filter(status='Pending')
        for wish in wishes:
            score = Match.calculate_match_score(wish, self)
            if score > self.match_percentage:
                self.match_percentage = score
                self.save(update_fields=['match_percentage'])  # Update the match_percentage field
                
                # Update the wish's match_percentage if the score is greater
                if score > wish.match_percentage:
                    wish.match_percentage = score
                    wish.save(update_fields=['match_percentage'])  # Save the updated match_percentage for the wish

    def send_match_email(self, wish, offer):
        subject = "Your Offer has been Matched!"
        html_message = render_to_string('email_templates/match_notification.html', {'wish': wish, 'offer': offer})
        plain_message = strip_tags(html_message)
        from_email = 'your_email@example.com'  # Replace with your email
        recipient_list = [wish.email, offer.email]  # Assuming both Wish and Offer have an email field

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

class Match(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, related_name='matches')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='matches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match_percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"Match: {self.wish.full_name} with {self.offer.full_name}"

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
        elif (wish.product and offer.product and 
              wish.product.category and offer.product.category and 
              wish.product.category == offer.product.category) or \
             (wish.service and offer.service and 
              wish.service.category and offer.service.category and 
              wish.service.category == offer.service.category):
            score += weights['category_match']

        max_score += max(weights['exact_match'], weights['category_match'])

        # Check title similarity
        title_similarity = SequenceMatcher(None, wish.title.lower(), offer.title.lower()).ratio()
        score += weights['title_similarity'] * title_similarity
        max_score += weights['title_similarity']

        # Calculate percentage
        percentage_score = round((score / max_score) * 100) if max_score > 0 else 0

        return percentage_score  # Return as an integer
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

   
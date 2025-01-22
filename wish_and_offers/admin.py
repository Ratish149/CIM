from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Service, Wish, Offer, Match, HSCode

@admin.register(HSCode)
class HSCodeAdmin(ModelAdmin):
    list_display = ['hs_code', 'description']
    search_fields = ['hs_code', 'description']
    ordering = ['hs_code']

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Wish)
class WishAdmin(ModelAdmin):
    list_display = ['title', 'full_name', 'product', 'service', 'type','status','match_percentage']
    list_filter = ['status', 'type']
    search_fields = ['title', 'full_name', 'product__hs_code']

@admin.register(Offer)
class OfferAdmin(ModelAdmin):
    list_display = ['title', 'full_name', 'product', 'service', 'type','status','match_percentage']
    list_filter = ['status', 'type']
    search_fields = ['title', 'full_name', 'product__hs_code']

@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = ['wish', 'offer', 'match_percentage', 'created_at']
    list_filter = ['created_at']
    search_fields = ['wish__title', 'offer__title']

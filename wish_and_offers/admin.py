from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product, Service,Wish,Offer,Match
# Register your models here.

admin.site.register(Category,ModelAdmin)
admin.site.register(Product,ModelAdmin)
admin.site.register(Service,ModelAdmin)
admin.site.register(Wish,ModelAdmin)
admin.site.register(Offer,ModelAdmin)
admin.site.register(Match,ModelAdmin)

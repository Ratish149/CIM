from django.db import models

# Create your models here.

class NatureOfIndustryCategory(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class NatureOfIndustrySubCategory(models.Model):
    category=models.ForeignKey(NatureOfIndustryCategory, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    def __str__(self):
        return f'{self.name} - {self.category.name}'


class MeroDeshMeraiUtpadan(models.Model):

    INDUSTRY_CHOICES=(
        ('Startup','Startup'),
        ('Micro','Micro'),
        ('Cottage','Cottage'),
        ('Small','Small'),
        ('Medium','Medium'),
        ('Large','Large'),
    )

    MARKET_CHOICES=(
        ('Domestic','Domestic'),
        ('International','International'),
        ('Both','Both'),
    )
    RAW_MATERIAL_CHOICES=(
        ('Local','Local'),
        ('International','International'),
        ('Both','Both'),
    )

    name_of_company=models.CharField(max_length=255)
    address_province=models.CharField(max_length=255)
    address_district=models.CharField(max_length=255)
    address_municipality=models.CharField(max_length=255)
    address_ward=models.CharField(max_length=255)
    address_street=models.CharField(max_length=255)
    contact_name=models.CharField(max_length=255)
    contact_number=models.CharField(max_length=255)
    contact_designation=models.CharField(max_length=255)
    contact_alternate_number=models.CharField(max_length=255,null=True,blank=True)
    contact_email=models.EmailField(null=True,blank=True)
    nature_of_industry_category=models.ForeignKey(NatureOfIndustryCategory, on_delete=models.CASCADE)
    nature_of_industry_sub_category=models.ForeignKey(NatureOfIndustrySubCategory, on_delete=models.CASCADE)
    
    is_other_manufacturing_industries=models.BooleanField(default=False,null=True,blank=True)
    is_hotel_and_other_service_industries=models.BooleanField(default=False,null=True,blank=True)
    is_It_service=models.BooleanField(default=False,null=True,blank=True)
    is_agro_NTFPs=models.BooleanField(default=False,null=True,blank=True)
    is_others=models.BooleanField(default=False,null=True,blank=True)

    product_market=models.CharField(max_length=255,choices=MARKET_CHOICES)
    raw_material=models.CharField(max_length=255,choices=RAW_MATERIAL_CHOICES)
    member_of_cim=models.BooleanField(default=False,null=True,blank=True)
    know_about_mdmu=models.BooleanField(default=False,null=True,blank=True)

    already_used_logo=models.BooleanField(default=False,null=True,blank=True)
    interested_in_logo=models.BooleanField(default=False,null=True,blank=True)

    self_declaration=models.BooleanField(default=False)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_of_company
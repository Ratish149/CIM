"""
URL configuration for CIM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/business_clinic/',include('business_clinic.urls')),
    path('api/mdmu/',include('mero_desh_merai_utpadan.urls')),
    path('api/koshi_quality_standard/',include('koshi_quality_standard.urls')),
    path('api/accounts/',include('accounts.urls')),
    path('api/business_registration/',include('business_registration.urls')),
    path('api/events/',include('events.urls')),
    path('api/wish_and_offers/',include('wish_and_offers.urls')),
    path('api/',include('contact.urls')),
    path('api/bds/',include('bds_service.urls')),
    path('api/business_information/',include('business_information.urls')),
    path('api/',include('stall_booking.urls')),
    path('api/',include('voting.urls')),
    path('api/',include('rojgar_pavillion.urls')),
    path('api/',include('stall_booking.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
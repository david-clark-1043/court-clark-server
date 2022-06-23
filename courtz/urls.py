"""courtz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from courtzapi import views
from django.urls import path, include

from django.conf import settings
from django.urls import re_path
from django.views.static import serve


router = DefaultRouter(trailing_slash=False)
router.register(r'filers', views.FilerView, 'filer')
router.register(r'filings', views.FilingView, 'filing')
router.register(r'filingTypes', views.FilingTypeView, 'filing_type')
router.register(r'partyTypes', views.PartyTypeView, 'party_type')
router.register(r'dockets', views.DocketView, 'docket')
router.register(r'firms', views.FirmView, 'firm')
router.register(r'repFirms', views.RepFirmView, 'rep_firm')
# router.register(r'f', views.FilingView, 'filing')

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register_user),
    path('login', views.login_user),
    path('admin/', admin.site.urls),
]

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
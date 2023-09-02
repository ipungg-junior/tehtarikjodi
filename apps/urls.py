from django.urls import path
from apps.views import LandingPage

urlpatterns = [
    path('', LandingPage.as_view(context="")),
    
]

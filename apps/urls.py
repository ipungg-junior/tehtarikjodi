from django.urls import path
from apps.views import LandingPage, Simulation, NotFoundPage

urlpatterns = [
    path('', LandingPage.as_view(context="")),
    path('simulasi-investasi/', Simulation.as_view(context="simulation")),
    path('simulasi-investasi/post-calculate/', Simulation.as_view(context="post-calculate")),
    path('simulasi-investasi/report/', Simulation.as_view(context="report-simulation")),
    path('404/', NotFoundPage.as_view(context=""))
]

from django.urls import path
from apps.views import LandingPage, Simulation, NotFoundPage, DashboardAdmin

urlpatterns = [
    path('', LandingPage.as_view(context="")),
    path('login/', DashboardAdmin.as_view(context="login")),
    path('insight/', DashboardAdmin.as_view(context="insight")),
    path('insight/detail/<int:id>/', DashboardAdmin.as_view(context="detail")),
    path('simulasi-investasi/', Simulation.as_view(context="simulation")),
    path('simulasi-investasi/post-calculate/', Simulation.as_view(context="post-calculate")),
    path('simulasi-investasi/report/', Simulation.as_view(context="report-simulation")),
    path('404/', NotFoundPage.as_view(context=""))
]

from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from cargo import views as cargo_views

router = routers.DefaultRouter()

router.register(r"cargo", cargo_views.CargoViewSet, basename="cargo")

urlpatterns = [
    
]

urlpatterns += router.urls

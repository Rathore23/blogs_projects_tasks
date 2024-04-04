from django.urls import path, include
from rest_framework import routers

from category.views import CategoryViewSet

router = routers.SimpleRouter()
router.register(r'', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]

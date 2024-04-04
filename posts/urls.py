from django.urls import path, include
from rest_framework import routers

from posts.views import PostViewSet, PostPhotosViewSet
from unicef_restlib.routers import NestedComplexRouter

router = routers.SimpleRouter()
router.register(r'', PostViewSet, basename='post')

post_router = NestedComplexRouter(router, r'')
post_router.register(r'photos', PostPhotosViewSet, basename='post-photos')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
]

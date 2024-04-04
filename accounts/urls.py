from django.urls import path, include
from rest_framework import routers

from accounts.views import RegistrationViewSet, UserAuthViewSet, AccountsViewSet

router = routers.SimpleRouter()
router.register(r'registration', RegistrationViewSet, basename='registration')
router.register(r'auth', UserAuthViewSet, basename='auth')
router.register(r'', AccountsViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]

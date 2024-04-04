from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from accounts.permissions import IsAdminOrReadOnly
from category.models import Category
from category.serializers import CategorySerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    # http_method_names = ("GET", )

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from category.models import Category
from utils.models import CommanModel
from utils.utils import get_post_photo_path


class Post(CommanModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_posts'
    )
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_posts'
    )
    liked_by = models.ManyToManyField(to=settings.AUTH_USER_MODEL,)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f"{self.id} - {self.title}"


class PostPhoto(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_photos'
    )
    image = models.ImageField(
        upload_to=get_post_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.image and (not self.width or not self.height):
            self.width = 300  # self.image.width in 300 pixels
            self.height = 300  # self.image.height in 300 pixels
        super().save(*args, **kwargs)

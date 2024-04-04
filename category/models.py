from django.db import models

from utils.models import CommanModel


class Category(CommanModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.title}"
    
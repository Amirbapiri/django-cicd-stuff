from django.db import models

from djangocicd.common.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from djangocicd.common.models import BaseModel


User = get_user_model()


class Post(BaseModel):
    slug = models.SlugField(primary_key=True, max_length=100)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )

    def __str__(self):
        return self.slug


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subs")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="targets")

    class Meta:
        unique_together = ("subscriber", "target")

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": {"'subscriber' and 'target' can not be equivalent"}})

    def __str__(self):
        return f"{self.subscriber.email} - {self.target.email}"


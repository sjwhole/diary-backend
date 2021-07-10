from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateField(auto_now_add=True)
    share = models.BooleanField(default=False)

    def __str__(self):
        return self.body

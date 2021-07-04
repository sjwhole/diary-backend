from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Post(models.Model):
    body = models.TextField()
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateField(auto_now_add=True)

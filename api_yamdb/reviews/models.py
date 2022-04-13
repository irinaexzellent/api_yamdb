from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Titles(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        'Titles',
        related_name='Titles_review',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    score = models.IntegerField(
        default=10,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])

    def __str__(self) -> str:
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        'Review',
        related_name='review_comments',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        related_name='comment',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

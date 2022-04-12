from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    comment = models.ForeignKey(
        'Comments',
        related_name='review_comments',
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

    def __str__(self) -> str:
        return self.text[:15]


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        related_name='comment',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

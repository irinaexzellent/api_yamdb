from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    ROLE = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')]

    role = models.CharField(
        max_length=5,
        choices=ROLE,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    username = models.CharField(
        max_length=150, unique=True, blank=False, null=False
    )
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False
    )

    confirmation_code = models.CharField(
        max_length=70,
        unique=True,
        blank=True,
        null=True,
        verbose_name='confirmation_code'
    )


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.confirmation_code = default_token_generator.make_token(
            user=instance
            )
        instance.save()

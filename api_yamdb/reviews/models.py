from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator


User = get_user_model


class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.SmallIntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
        related_name='title',
    )
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
    )


class Category(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.SlugField(unique=True)


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre_title',
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_title',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='unique_GenreTitle'
            )
        ]


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

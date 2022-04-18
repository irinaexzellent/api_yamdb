from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models


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

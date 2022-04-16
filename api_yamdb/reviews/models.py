from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model

class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.SmallIntegerField()
    desription = models.TextField()
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
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
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

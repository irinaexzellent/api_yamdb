import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Модель пользователей."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')]

    role = models.CharField(
        'роль',
        max_length=5,
        choices=ROLE,
        default=USER,
    )

    bio = models.TextField(
        'биография',
        blank=True,
    )

    username = models.CharField(
        'имя', max_length=150, unique=True, blank=False, null=False
    )
    email = models.EmailField(
        'емэйл', max_length=254, unique=True, blank=False, null=False
    )

    confirmation_code = models.CharField(
        max_length=70,
        unique=True,
        blank=True,
        null=True,
        verbose_name='confirmation_code'
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.confirmation_code = default_token_generator.make_token(
            user=instance
        )
        instance.save()


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField('название', max_length=250)
    year = models.PositiveSmallIntegerField(
        'год',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(
                datetime.datetime.now().year,
                message='Нельзя добавлять произведения, которые еще не вышли',
            )
        ],
    )
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
        related_name='title',
        verbose_name='категория',
    )
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        verbose_name='жанр',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField('название категории', max_length=256,)
    slug = models.SlugField('ссылка', unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField('название жанра', max_length=256,)
    slug = models.SlugField('ссылка', unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class GenreTitle(models.Model):
    """Модель жанров произведений."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre_title_id',
        verbose_name='произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_title',
        verbose_name='жанр',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_GenreTitle'
            )
        ]
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        related_name='Titles_review',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
    )
    text = models.TextField('текст',)
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        'оценка',
        default=10,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author_id'],
                name='unique_reviews'
            )
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class Comments(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        related_name='review_comments',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='отзыв',
    )
    author = models.ForeignKey(
        'User',
        related_name='comment',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='автор',
    )
    text = models.TextField('текст',)
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

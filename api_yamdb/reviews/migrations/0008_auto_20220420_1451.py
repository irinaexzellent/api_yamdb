# Generated by Django 2.2.16 on 2022-04-20 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220420_0820'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='genretitle',
            name='unique_GenreTitle',
        ),
        migrations.RenameField(
            model_name='genretitle',
            old_name='genre_id',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='genretitle',
            old_name='title_id',
            new_name='title',
        ),
        migrations.AddConstraint(
            model_name='genretitle',
            constraint=models.UniqueConstraint(fields=('title', 'genre'), name='unique_GenreTitle'),
        ),
    ]

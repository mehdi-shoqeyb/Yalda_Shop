# Generated by Django 4.2.4 on 2024-08-17 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_module', '0020_alter_productcomment_dis_likes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcomment',
            name='dis_likes',
        ),
        migrations.RemoveField(
            model_name='productcomment',
            name='likes',
        ),
        migrations.AddField(
            model_name='productcomment',
            name='dis_likes',
            field=models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='دیس لایک'),
        ),
        migrations.AddField(
            model_name='productcomment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL, verbose_name='لایک'),
        ),
    ]

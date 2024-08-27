# Generated by Django 4.2.4 on 2024-08-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0019_rename_di_likes_productcomment_dis_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='dis_likes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='دیس لایک'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='likes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='لایک'),
        ),
    ]

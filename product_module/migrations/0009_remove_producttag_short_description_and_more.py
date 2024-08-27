# Generated by Django 4.2.4 on 2024-08-15 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0008_productgallery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttag',
            name='short_description',
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه'),
        ),
    ]

# Generated by Django 4.2.4 on 2024-08-12 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttag',
            name='url_title',
            field=models.CharField(db_index=True, default=True, max_length=300, verbose_name='عنوان در url'),
            preserve_default=False,
        ),
    ]

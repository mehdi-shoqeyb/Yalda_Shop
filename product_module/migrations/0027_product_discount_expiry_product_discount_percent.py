# Generated by Django 4.2.4 on 2024-08-18 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0026_product_sales_count_product_view_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_expiry',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضا تخفیف'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='درصد تخفیف'),
        ),
    ]

# Generated by Django 4.2.4 on 2024-08-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0017_alter_productcomment_di_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='cons',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='نقات منفی'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='pros',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='نقات مثبت'),
        ),
    ]

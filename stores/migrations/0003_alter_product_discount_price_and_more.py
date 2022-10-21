# Generated by Django 4.1.2 on 2022-10-07 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_category_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='view_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]

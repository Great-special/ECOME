# Generated by Django 4.1.2 on 2022-11-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0006_remove_product_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]

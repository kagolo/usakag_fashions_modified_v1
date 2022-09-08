# Generated by Django 4.1 on 2022-09-06 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_price_0_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_0',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
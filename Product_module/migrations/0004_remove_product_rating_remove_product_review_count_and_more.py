# Generated by Django 4.2.6 on 2025-01-04 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product_module', '0003_product_rating_product_review_count_product_sku_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='product',
            name='review_count',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product_module.productcategory', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, db_index=True, null=True, verbose_name='توضیحات اصلی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/products', verbose_name='تصویر'),
        ),
        migrations.DeleteModel(
            name='ProductGallery',
        ),
    ]

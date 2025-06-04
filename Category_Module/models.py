from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=150 , verbose_name= 'نام دسته بندی')
    slug = models.SlugField(max_length=150 , verbose_name='slug')
    parent = models.ForeignKey('Category',on_delete=models.CASCADE , null=True , blank=True , verbose_name= 'نام والد')
    def __str__(self):
        return self.title
    class META:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


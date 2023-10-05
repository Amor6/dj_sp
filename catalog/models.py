from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

NULLABLE = {'null': True, 'blank': True}
User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='категория')
    description = models.TextField(**NULLABLE, verbose_name="описание")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    product_name = models.CharField(max_length=250, verbose_name="наименование")
    description = models.TextField(verbose_name="описание"),
    preview_img = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='превью')
    category = models.ForeignKey(Category, **NULLABLE, on_delete=models.CASCADE, verbose_name="категория")
    price = models.IntegerField(verbose_name='цена')
    creation_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    last_change_date = models.DateField(auto_now=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return f'Название: {self.product_name} (Категория:{self.category}): Цена:{self.price}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

        permissions = [
            (
                'set_published',
                'Can publish posts'
            ),
            (
                'set_category',
                'Can change category'
            ),
            (
                'set_description',
                'Can change description'
            ),
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, **NULLABLE, on_delete=models.CASCADE, verbose_name="продукт")
    version_number = models.CharField(max_length=150, verbose_name='номер версии')
    version_name = models.CharField(max_length=150, verbose_name='название версии')
    version_sing = models.BooleanField(default=False, verbose_name='признак текущей версии')


class Record(models.Model):
    record_title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(max_length=15000, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='image/', verbose_name='Изображение', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    sign_of_publication = models.BooleanField(default=True, verbose_name='Признак публикации')
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.record_title

    def get_absolute_url(self):
        return reverse('record_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        ordering = ('record_title', 'slug', 'created_at', 'sign_of_publication')

    def increase_views(self):
        self.views += 1
        self.save()

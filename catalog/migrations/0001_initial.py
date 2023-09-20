# Generated by Django 4.2.5 on 2023-09-20 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='категория')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250, verbose_name='наименование')),
                ('preview_img', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='превью')),
                ('price', models.IntegerField(verbose_name='цена')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='дата создания')),
                ('last_change_date', models.DateField(auto_now=True, verbose_name='дата последнего изменения')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'permissions': [('set_published', 'Can publish posts'), ('set_category', 'Can change category'), ('set_description', 'Can change description')],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.CharField(max_length=150, verbose_name='номер версии')),
                ('version_name', models.CharField(max_length=150, verbose_name='название версии')),
                ('version_sing', models.BooleanField(default=False, verbose_name='признак текущей версии')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
    ]

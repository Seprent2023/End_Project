# Generated by Django 4.2.6 on 2024-03-23 06:32

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Category name', max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_post', models.CharField(choices=[('TK', 'Танки'), ('HL', 'Хилеры'), ('DD', 'ДД'), ('MR', 'Торговцы'), ('GM', 'Гильдмастера'), ('QG', 'Квестгиверы'), ('SM', 'Кузнецы'), ('LW', 'Кожевники'), ('PM', 'Зельевары'), ('EH', 'Мастера заклинаний')], default='MR', max_length=2, verbose_name='Время публикации')),
                ('time_in', models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')),
                ('headline', models.CharField(max_length=128, verbose_name='Заголовок')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='PostBoard_main.category', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='PostBoard_main.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('res_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='PostBoard_main.posts', verbose_name='Пост')),
                ('res_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_user', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='RegUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default=None, max_length=6, null=True)),
                ('reg_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='posts',
            name='to_reg_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PostBoard_main.regusers', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='category',
            name='subscriber',
            field=models.ManyToManyField(through='PostBoard_main.Subscriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]

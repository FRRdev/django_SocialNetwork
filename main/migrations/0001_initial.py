# Generated by Django 3.1.7 on 2021-04-24 21:26

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(db_index=True, max_length=20, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия пользователя')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='почта')),
                ('image', models.ImageField(blank=True, null=True, upload_to=main.utilities.get_timestamp_path, verbose_name='Изображение')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name='Телефон')),
                ('date_of_birth', models.DateField(blank=True, max_length=8, null=True, verbose_name='Дата рождения')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='Город')),
                ('about_me', models.TextField(blank=True, max_length=200, null=True, verbose_name='Обо мне')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000, verbose_name='Контент')),
                ('from_user', models.CharField(max_length=30, verbose_name='Отправитель')),
                ('data_of_mes', models.DateTimeField(auto_now_add=True, verbose_name='Отправлено')),
                ('is_active', models.BooleanField(default=True, verbose_name='Прочитано?')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-data_of_mes'],
            },
        ),
    ]
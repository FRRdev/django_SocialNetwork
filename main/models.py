from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .utilities import get_timestamp_path
from django.contrib.auth import get_user_model


class SocialUser(AbstractUser):
    ''' Social network user '''
    first_name = models.CharField(max_length=20,db_index=True,verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=20,verbose_name='Фамилия пользователя')
    email = models.EmailField(null=True,blank=True,verbose_name='почта')
    image = models.ImageField(null=True,blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    phone = models.CharField(max_length=12,null=True,blank=True,verbose_name='Телефон')
    date_of_birth = models.DateField(max_length=8,null=True,blank=True,verbose_name='Дата рождения')
    city = models.CharField(max_length=20,null=True,blank=True,verbose_name='Город')
    about_me = models.TextField(max_length=200,null=True,blank=True,verbose_name='Обо мне')
    class Meta(AbstractUser.Meta):
        pass

class Message(models.Model):
    ''' Message '''
    to_user = models.ForeignKey(SocialUser,on_delete=models.CASCADE,verbose_name='Получатель')
    content = models.TextField(max_length=1000,verbose_name='Контент')
    from_user = models.CharField(max_length=30,verbose_name='Отправитель')
    data_of_mes = models.DateTimeField(auto_now_add=True, verbose_name='Отправлено')
    is_active = models.BooleanField(default=True,verbose_name='Прочитано?')
    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = 'Сообщение'
        ordering = ['-data_of_mes']

class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    


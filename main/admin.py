# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import SocialUser,Message,City


admin.site.register(SocialUser)
admin.site.register(Message)
admin.site.register(City)
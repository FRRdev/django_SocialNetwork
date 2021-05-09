from django.urls import path
from .views import index,CCLoginView,profile,ChangeUserInfoView,CCPasswordChangeView,CCLogoutView,RegisterUserView,AllPeopleView
from .views import send_message,ShowMessageView,read_message,delete_message,show_weather
app_name = 'main'

urlpatterns = [
    path('people/',AllPeopleView.as_view(),name='people'),
    path('people/<int:from_pk>/<int:to_pk>/',send_message,name='send_message'),
    path('messages/<int:pk>/',ShowMessageView.as_view(),name='show_messages'),
    path('messages/detail/<int:pk>/',read_message,name='detail_mes'),
    path('accounts/logout/',CCLogoutView.as_view(),name='logout'),
    path('delete/messages/<int:pk>/',delete_message,name='delete_message'),
    path('accounts/register/',RegisterUserView.as_view(),name='register'),
    path('accounts/profile/change/',ChangeUserInfoView.as_view(),name='profile_change'),
    path('accounts/password/change/',CCPasswordChangeView.as_view(),name='password_change'),
    path('accounts/profile/',profile,name='profile'),
    path('accounts/login/',CCLoginView.as_view(),name='login'),
    path('weather/',show_weather,name='weather'),
    path('',index,name='index'),
]
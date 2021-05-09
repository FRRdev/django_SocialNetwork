from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.views import LoginView,PasswordChangeView,LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from .models import SocialUser,Message,City
from django.urls import reverse_lazy
from django.views.generic import View,DetailView
from .forms import ChangeUserInfoForm,RegisterUserForm,SendMessageForm,CityForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponseNotFound
import requests

def index(request):
    return render(request,'main/index.html',{})

class CCLoginView(LoginView):
    template_name = 'main/login.html'

class CCLogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'main/logout.html'

@login_required
def profile(request):
    return render(request, 'main/profile.html')

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SocialUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class CCPasswordChangeView(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль изменен!'

class RegisterUserView(CreateView):
    model = SocialUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:profile')

class AllPeopleView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        user_pk = request.user.pk
        people = SocialUser.objects.exclude(pk=user_pk)
        paginator = Paginator(people, 3)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {'people':page.object_list,'page':page}
        return render(request,'main/allpeople.html',context)

@login_required
def send_message(request,from_pk,to_pk):
    to_user = get_object_or_404(SocialUser,pk=to_pk)
    from_user = request.user
    from_user = from_user.first_name + " " + from_user.last_name
    initial = {'to_user':to_user,'from_user':from_user}
    form = SendMessageForm(initial=initial)
    if request.method == 'POST':
        s_form = SendMessageForm(request.POST)
        if s_form.is_valid():
            s_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Сообщение отправлено')
            redirect('main:people')

    context = {'to_user':to_user,'form': form}
    return render(request, 'main/sendmessage.html', context)

class ShowMessageView(LoginRequiredMixin,View):
    def get(self,request,pk):
        user = get_object_or_404(SocialUser,pk=pk)
        all_msg = user.message_set.all()
        paginator = Paginator(all_msg,7)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        msgs_active = user.message_set.filter(is_active=True)
        msgs_noact = user.message_set.filter(is_active=False)
        context = {
            'msgs_active':msgs_active,
            'msgs_noact':msgs_noact,
            'all_msg':page.object_list,
            'page':page
        }
        return render(request,'main/showmessages.html',context)

@login_required
def read_message(request,pk):
    message = get_object_or_404(Message,pk=pk)
    if message.is_active:
        message.is_active = False
        message.save()
    context = {'message':message}
    return render(request,'main/detail_message.html',context)

@login_required
def delete_message(request,pk):
    try:
        message = Message.objects.get(pk=pk)
        message.delete()
        return redirect('main:profile')
    except Message.DoesNotExist:
        return HttpResponseNotFound("<h2>Message not found</h2>")


def show_weather(request):
    key = '94a056f1456145389547da34eb2db50a'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + key

    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.order_by('-id')[:5]
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city':city.name,
            'temp':res['main']['temp'],
            'icon':res['weather'][0]['icon'],
        }
        all_cities.append(city_info)
    context = {
       'all_info':all_cities,
        'form':form,
    }
    return render(request,'main/weather.html',context)


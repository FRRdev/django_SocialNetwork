from django import forms
from .models import SocialUser,Message,City
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class ChangeUserInfoForm(forms.ModelForm):
    ''' Form for changing user information '''
    email = forms.EmailField(required=True, label='Адрес электронной почты') #полное обьявление
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.widgets.DateInput(attrs={'type':'date',}))
    about_me = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':4, 'cols':20}),label='Обо мне')
    class Meta:
        model = SocialUser
        fields = ('email','phone','image','first_name', 'last_name', 'date_of_birth','city','about_me') #быстрое обьявление


class RegisterUserForm(forms.ModelForm):
    ''' Form for registering a new user '''
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.widgets.DateInput(attrs={'type': 'date', }))
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                help_text='Введите тот же самый пароль еще раз для проверки')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save() # отослат польз письмо с треб актвации
        return user

    def clean_password1(self): #выполняем валидацию пароля введенное в первое поле
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self): # проверяем совпадают ли пароли
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают',
                                  code='password_mismatch')}
            raise ValidationError(errors)


    class Meta:
        model = SocialUser
        fields = ('username','email', 'password1', 'password2', 'first_name', 'last_name','phone','city','image','date_of_birth')

class SendMessageForm(forms.ModelForm):
    ''' Form for sending a message '''
    content = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':4, 'cols':20}),label='Напишите сообщение')
    class Meta:
        model = Message
        exclude = ('is_active',)
        widgets = {'is_active': forms.HiddenInput,
                   'to_user': forms.HiddenInput,
                   'from_user': forms.HiddenInput,
                   'data_of_mes': forms.HiddenInput}

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name':forms.TextInput(attrs={
            'class':'form-control',
            'name':'city',
            'id':'city',
            'placeholder':'Введите город',
        })}
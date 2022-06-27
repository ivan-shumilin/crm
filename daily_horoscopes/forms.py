# from django import forms
#
#
# class CreateUsersForms(forms.Form):
#     email = forms.EmailField(max_length=100, label="Email")
#     username = forms.CharField(max_length=100, label="Имя пользователя",
#                                widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password = forms.CharField(max_length=100, label="Пароль",
#                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
# нужно использовать поле passwordInput
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm, DateInput

class TimetableForm(ModelForm):
    class Meta:
        model = Timetable
        fields = ['datetime']

        widgets = {
            "datetime": DateInput(attrs={
                'type': 'date',
                'class': 'form-conrol',
            })
        }

# class ProductForm(forms.ModelForm):
#     ovd = forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'})
#     shd = forms.CheckboxInput(
#         attrs={'class': 'form-check-input', 'type': 'checkbox'})
#     bd = forms.CheckboxInput(
#         attrs={'class': 'form-check-input', 'type': 'checkbox'})
#     vbd = forms.CheckboxInput(
#         attrs={'class': 'form-check-input', 'type': 'checkbox'})
#     nbd = forms.CheckboxInput(
#         attrs={'class': 'form-check-input', 'type': 'checkbox'})
#     nkd = forms.CheckboxInput(
#         attrs={'class': 'form-check-input', 'type': 'checkbox'})
#     vkd = forms.CheckboxInput(
#         attrs={'class': 'form-check-input', 'type': 'checkbox'})
#     name = forms.CharField(widget=forms.TextInput(attrs={'style': "display: none;"}), required=False)
#     description = forms.CharField(widget=forms.TextInput(attrs={'style': "display: none;"}), required=False)
#     carbohydrate = forms.CharField(widget=forms.TextInput(attrs={'style': "display: none;"}), required=False)
#     iditem = forms.CharField(widget=forms.TextInput(attrs={'style': "display: none;"}), required=False)
#     fat = forms.CharField(widget=forms.TextInput(attrs={'style': "display: none;"}), required=False)
#     fiber = forms.CharField(widget=forms.TextInput(attrs={'style': "display: none;"}), required=False)
#     energy = forms.CharField(widget=forms.TextInput(attrs={'style': "display: none;"}), required=False)
#
#     class Meta:
#         model = Product
#         fields = ('iditem', 'name', 'description', 'ovd', 'shd', 'bd', 'vbd', 'nbd', 'nkd',
#                      'vkd', 'carbohydrate', 'fat', 'fiber', 'energy')


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль еще раз'}))

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class UserloginForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    # attrs = {'class': 'form-control'}
    class Meta:
        model = User
        fields = ('username', 'password')

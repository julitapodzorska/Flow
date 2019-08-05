from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(label = "Nazwa użytkownika", max_length=64)
    first_name = forms.CharField(label="Imię",max_length=30, required=True)
    last_name = forms.CharField(label="Nazwisko",max_length=30, required=True)
    email = forms.EmailField(label="E-mail",max_length=254, required=True)
    last_cycle = forms.DateField(widget=forms.SelectDateWidget, label="Data ostatniego cyklu",required=True, help_text="Data rozpoczęcia ostatniego krwawienia.")
    avg_cycle = forms.IntegerField(widget=forms.NumberInput,label="Srednia długość cyklu", required=True, help_text="Cykl rozpoczyna się pierwszego dnia krwawienia i kończy pierwszego dnia następnego krwawienia.")
    password1 = forms.CharField(widget= forms.PasswordInput,label="Hasło", max_length=64)
    password2 = forms.CharField(widget= forms.PasswordInput, label="Powtórz hasło", max_length=64)

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields+('email', 'first_name', 'last_name', 'last_cycle', 'avg_cycle')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = UserCreationForm.Meta.fields+('email', 'first_name', 'last_name', 'last_cycle', 'avg_cycle')


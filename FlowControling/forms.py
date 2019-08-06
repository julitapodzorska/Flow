from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, HealthData, BLEEDING, PAIN, MOOD, SEX, ENERGY


DATE = (

        (0, 'Dziś'),
        (1, 'Wczoraj'),
        (2, 'Przedwczoraj'),

)





class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label = "Nazwa użytkownika", max_length=64)
    first_name = forms.CharField(label="Imię",max_length=30, required=True)
    last_name = forms.CharField(label="Nazwisko",max_length=30, required=True)
    email = forms.EmailField(label="E-mail",max_length=254, required=True)
    last_cycle = forms.DateField(widget=forms.SelectDateWidget, label="Data ostatniego cyklu",required=True, help_text="Data rozpoczęcia ostatniego krwawienia.")
    avg_cycle = forms.IntegerField(widget=forms.NumberInput,label="Średnia długość cyklu", required=True, help_text="Cykl rozpoczyna się pierwszego dnia krwawienia i kończy pierwszego dnia następnego krwawienia.")
    password1 = forms.CharField(widget= forms.PasswordInput,label="Hasło", max_length=64)
    password2 = forms.CharField(widget= forms.PasswordInput, label="Powtórz hasło", max_length=64)

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields+('email', 'first_name', 'last_name', 'last_cycle', 'avg_cycle')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = UserCreationForm.Meta.fields+('email', 'first_name', 'last_name', 'last_cycle', 'avg_cycle')


class HealthForm(forms.Form):
    bleeding = forms.ChoiceField(choices=BLEEDING, label="Krwawienie")
    pain = forms.ChoiceField(choices=PAIN, label="Ból")
    mood = forms.ChoiceField(choices=MOOD, label="Nastrój")
    sex = forms.ChoiceField(choices=SEX, label="Seks")
    energy = forms.ChoiceField(choices=ENERGY, label="Poziom energii")
    date = forms.ChoiceField(choices=DATE, label="Dzień")



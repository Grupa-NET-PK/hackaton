from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Flashcard


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class FlashcardCreateForm(forms.ModelForm):
    visibility = forms.BooleanField()
    question = forms.CharField(label='Jakie pytanie chcesz zadać ?', widget=forms.TextInput(attrs={'placeholder': 'Zadaj pytanie'}))
    is_abcd = forms.BooleanField()
    a = forms.CharField(label='Opcja A', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje A'}))
    b = forms.CharField(label='Opcja B', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje B'}))
    c = forms.CharField(label='Opcja C', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje D'}))
    d = forms.CharField(label='Opcja D', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje C'}))
    correct_answer = forms.CharField(label='Poprawna odpowiedz', widget=forms.TextInput(attrs={'placeholder': 'Podaj odpowiedz'}))

    class Meta:
        model = Flashcard
        fields = ['visibility', 'question', 'is_abcd', 'a', 'b', 'c', 'd', 'correct_answer']


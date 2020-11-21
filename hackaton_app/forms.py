import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Flashcard, AssignedFlashcard, AnswerFlashcard


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
    ABCD_CHOICES = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    )
    visibility = forms.BooleanField(label="Widoczność", required=False)
    question = forms.CharField(label='Jakie pytanie chcesz zadać ?', widget=forms.TextInput(attrs={'placeholder': 'Zadaj pytanie'}))
    is_abcd = forms.BooleanField(widget=forms.HiddenInput(),label="ABCD", required=False)
    a = forms.CharField(label='Opcja A', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje A'}), required=False)
    b = forms.CharField(label='Opcja B', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje B'}), required=False)
    c = forms.CharField(label='Opcja C', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje D'}), required=False)
    d = forms.CharField(label='Opcja D', widget=forms.TextInput(attrs={'placeholder': 'Podaj opcje C'}), required=False)
    abcd_answer = forms.CharField(
        label="Poprawna odpowiedź",
        max_length=1,
        required=False,
        widget=forms.Select(choices=ABCD_CHOICES)
        )
    correct_answer = forms.CharField(label='Poprawna odpowiedz', widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Flashcard
        fields = ['question', 'a', 'b', 'c', 'd', 'abcd_answer', 'visibility']


class FlashcardCreateOQForm(forms.ModelForm):
    question = forms.CharField(label='Jakie pytanie chcesz zadać ?', widget=forms.TextInput(attrs={'placeholder': 'Zadaj pytanie'}))
    is_abcd = forms.BooleanField(widget=forms.HiddenInput(),label="ABCD", required=False, initial=False)
    is_openquestion = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=True)
    correct_answer = forms.CharField(label='Proponowana odpowiedz', widget=forms.TextInput(attrs={'placeholder': 'Podaj odpowiedz'}), required=False)
    visibility = forms.BooleanField(label="Widoczność", required=False)

    class Meta:
        model = Flashcard
        fields = ['question', 'correct_answer', 'visibility']


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'a', 'b', 'c', 'd', 'abcd_answer', 'visibility']


class AnswerFlashcardForm(forms.ModelForm):
    answer = forms.CharField(label='Twoja odpowiedz', widget=forms.TextInput(attrs={'placeholder': 'Podaj odpowiedz'}))


class AssignFlashcardForm(forms.ModelForm):

    def __init__(self, userid, *args, **kwargs):
        super(AssignFlashcardForm, self).__init__(*args, **kwargs)
        self.fields['flash_card'].queryset = Flashcard.objects.filter(user_id=userid)
        self.fields['user'].queryset = Profile.objects.all()#exclude(id=userid)

    class Meta:
        model = AssignedFlashcard
        fields = ['user', 'flash_card', 'expiration_date']


class AnswerFlashcardCreate(forms.ModelForm):
    class Meta:
        model = AnswerFlashcard
        fields = ['answer']

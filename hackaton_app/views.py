from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FlashcardCreateForm, AssignFlashcardForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import *


def home(request):
    context = {'title': 'Strona Główna'}
    return render(request, 'hackaton_app/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Twoje konto zostało utworzone, możesz się zalogować {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'hackaton_app/register.html', {'form': form, 'title': 'Rejestracja'})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Twoje konto zostało zaktualizowane!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Profil'
    }

    return render(request, 'hackaton_app/profile.html', context)

@login_required
def flashcard_create(request):
    if request.method == 'POST':
        f_form = FlashcardCreateForm(data=request.POST)
        if f_form.is_valid():
            instance = f_form.save(commit=False)
            instance.user = request.user.profile
            instance.save()
            messages.success(request, f'Utworzono Fiszkę!')
            return redirect('flashcard_show')
    else:
        f_form = FlashcardCreateForm()

    context = {
        'f_form': f_form,
    }

    return render(request, 'hackaton_app/flashcard_create.html', context)


class FlashcardListView(LoginRequiredMixin, ListView):
    model = Flashcard
    template_name = 'hackaton_app/flashcard_list.html'
    context_object_name = 'flash'

    def get_queryset(self):
        flash = Flashcard.objects.filter(user=self.request.user.profile)
        paginator = Paginator(flash, 10)
        page = self.request.GET.get('page')
        try:
            flash = paginator.page(page)
        except PageNotAnInteger:
            flash = paginator.page(1)
        except EmptyPage:
            flash = paginator.page(paginator.num_pages)
        return flash
    

class AssignedFlashcardListView(LoginRequiredMixin, ListView):
    model = AssignedFlashcard
    template_name = 'hackaton_app/assigned_flashcard_list.html'
    context_object_name = 'flash'

    def get_queryset(self):
        # filter_val = self.request.GET.get('filter', 'give-default-value')
        # order = self.request.GET.get('orderby', 'give-default-value')
        # user = get_object_or_404(User, username=self.kwargs.get["username"])
        new_context = AssignedFlashcard.objects.filter(
            user_id=self.request.user.id,
        )
        return new_context


@login_required
def flashcard_assign(request):
    if request.method == 'POST':
        f_form = AssignFlashcardForm(request.POST)
        if f_form.is_valid():
            instance = f_form.save(commit=False)
            instance.user = request.user.profile
            instance.save()
            messages.success(request, f'Przypisano fiszkę!')
            return redirect('profile')
    else:
        f_form = AssignFlashcardForm()

    return render(request, 'hackaton_app/assign_flashcard.html', {'form': f_form})



Flashcard_ListView = FlashcardListView.as_view()

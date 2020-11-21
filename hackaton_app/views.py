from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FlashcardCreateForm,FlashcardCreateOQForm, AssignFlashcardForm, AnswerFlashcardCreate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *


def home(request):
    context = {'title': 'Strona Główna', "user_id": request.user.id}
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

@login_required
def flashcard_create_oquestion(request):
    if request.method == 'POST':
        f_form = FlashcardCreateOQForm(data=request.POST)
        if f_form.is_valid():
            instance = f_form.save(commit=False)
            instance.is_openquestion = True
            instance.is_abcd = False
            instance.user = request.user.profile
            instance.save()
            messages.success(request, f'Utworzono Fiszkę!')
            return redirect('flashcard_show')
    else:
        f_form = FlashcardCreateOQForm()

    context = {
        'f_form': f_form,
    }

    return render(request, 'hackaton_app/flashcard_create_oquestion.html', context)


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
        f_form = AssignFlashcardForm(request.user.id, request.POST)
        if f_form.is_valid():
            instance = f_form.save(commit=False)
            # instance.user = request.user.profile
            instance.save()
            messages.success(request, f'Przypisano fiszkę!')
            return redirect('assigned_flashcard_show')
    else:
        f_form = AssignFlashcardForm(request.user.id)

    return render(request, 'hackaton_app/assign_flashcard.html', {'form': f_form})


@login_required
def check_assigned_flashcards(request):
    result = AssignedFlashcard.objects.filter(user_id=request.GET.get('userid'))

    html = render_to_string('hackaton_app/assigned_flashcard.html', {'flash': result})    
    return HttpResponse(html)



@login_required
def flashcard_answer_create(request, pk):
    if request.method == 'POST':
        f_form = AnswerFlashcardCreate(data=request.POST)
        if f_form.is_valid():
            instance = f_form.save(commit=False)
            instance.user = request.user.profile
            instance.flash_card = Flashcard.objects.get(id=pk)
            instance.save()
            messages.success(request, f'Utworzono Fiszkę!')
            return redirect('flashcard_show')
    else:
        f_form = AnswerFlashcardCreate()

    context = {
        'f_form': f_form,
    }

    return render(request, 'hackaton_app/flashcard_answer_create.html', context)


class FlashcardDetailView(DetailView):
    model = Flashcard
    template = 'hackaton_app/flashcard_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        akt_flashcard = get_object_or_404(Flashcard, id=self.kwargs['pk'])
        answers = AnswerFlashcard.objects.filter(flash_card=akt_flashcard)
        context['flash'] = akt_flashcard
        context['flash_ans'] = answers
        return context


class FlashcardUpdateView(UpdateView):
    model = Flashcard
    fields = ['question', 'a', 'b', 'c', 'd', 'abcd_answer', 'visibility']
    template_name_suffix = '_update_your_flash'


class FlashcardDeleteView(DeleteView):
    model = Flashcard
    success_url = reverse_lazy('home')

    
Flashcard_ListView = FlashcardListView.as_view()
Flashcard_UpdateView = FlashcardUpdateView.as_view()
Flashcard_DeleteView = FlashcardDeleteView.as_view()
Flashcard_DetailView = FlashcardDetailView.as_view()


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Quiz
from .filters import QuizFilter


class QuizDetailView(DetailView):
    model = Quiz


class QuizShowView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_show.html'


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.INFO, 'Your Quiz has been successfully created.')
        return super().form_valid(form)


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'quizzes'
    ordering = ['-date_created']        # - to inverse ordering
    # paginate_by = 3                     # number of quizzes per page

    # Filter -> Method 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = QuizFilter(self.request.GET, queryset=self.get_queryset())
        return context


class UserQuizListView(ListView):
    model = Quiz
    template_name = 'quiz/user_quiz.html'   # <app>/<model>_<viewtype>.html
    context_object_name = 'quizzes'
    ordering = ['-date_created']            # - to inverse ordering
    # paginate_by = 3                         # number of quizzes per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Quiz.objects.filter(author=user).order_by('-date_created')


class QuizEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    fields = ['course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.INFO, 'Your Quiz has been successfully updated.')
        return super().form_valid(form)

    def test_func(self):
        quiz = self.get_object()
        if self.request.user == quiz.author:
            return True
        else:
            return False


class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    success_url = '/'

    def test_func(self):
        quiz = self.get_object()
        if self.request.user == quiz.author:
            return True
        else:
            return False
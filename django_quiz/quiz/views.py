from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Quiz


class QuizDetailView(DetailView):
    model = Quiz


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'duration']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'quizzes'
    ordering = ['-date_created']         # - to inverse ordering
    paginate_by = 10                     # number of posts per page


class UserQuizListView(ListView):
    model = Quiz
    template_name = 'quiz/user_quiz.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'quizzes'
    paginate_by = 4                         # number of quizzes per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Quiz.objects.filter(author=user).order_by('-date_created')


class QuizEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    fields = ['course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'duration']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
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
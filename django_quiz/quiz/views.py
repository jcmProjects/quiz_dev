from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Quiz
from .filters import QuizFilter
from users.models import Course, ProfileCourse, Profile
from itertools import chain

import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


class QuizDetailView(DetailView):
    model = Quiz


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image'] # course

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
        auth_user = self.request.user;
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        auth_user_courses = ProfileCourse.objects.filter(profile_id=auth_user.id)
        user_courses = ProfileCourse.objects.filter(profile_id=user.id)

        print("{}".format( Quiz.objects.filter(author=user).filter(course__id=auth_user.id).order_by('-date_created') ))
        print("auth_user = {}".format(auth_user))
        print("page_user = {}".format(user))
        print("auth_user_courses = {}".format(auth_user_courses))
        print("page_user_courses = {}".format(user_courses))

        print( Quiz.objects.filter(author=user).filter(course__course_name="Teste") )   # Perguntas do author "user" com curso "Teste"
        print( Course.objects.filter(profile=auth_user.id) )                            # Cursos do auth_user

        # Encadear querysets
        q2 = Course.objects.filter(profile=auth_user.id).values_list('course_name')
        q1 = Quiz.objects.filter(course__course_name=q2[1])
        print(q2)
        print(q1)

        #* IT'S WORKING (i think)
        q3 = Course.objects.filter(profile=auth_user.id)
        q4 = Quiz.objects.filter(author=user).filter(course__in=q3)
        print(q3)
        print(q4)
        #* --------------------------------------------------------

        #return Quiz.objects.filter(author=user).order_by('-date_created')
        return q4.order_by('-date_created')
        


class QuizEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    fields = ['course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image'] # course

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


@csrf_exempt
@require_http_methods(["POST"])
def start_quiz(request, *args, **kwargs):
    #! study why this returns error:
    #json_data = json.loads(request.body)
    print("Test: ")# + json_data.quiz_id)

    to_return = {'type': 'success', 'msg': 'done', 'code': 200}
    return HttpResponse(json.dumps(to_return), content_type='application/json')


# Respostas vindas do microcontrolador
@csrf_exempt
@require_http_methods(["POST"])
def receive_response(request):
    date_now = datetime.datetime.now()

    json_data = json.loads(request.body)


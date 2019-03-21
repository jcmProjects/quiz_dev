import re   # for Start Quiz
from tablib import Dataset  # for Quiz Upload
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#from django.db.models import Q

from .models import Quiz, Answer, Results
from .forms import ChooseCourseForm, QuizUploadForm
from .filters import QuizFilter
from users.models import Course, ProfileCourse, Profile
from .resources import QuizResource

# Abade
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


class QuizDetailView(DetailView):
    model = Quiz

    def get_queryset(self):
        auth_user = self.request.user;

        # SubQueries - https://stackoverflow.com/questions/8556297/how-to-subquery-in-queryset-in-django
        q1 = Course.objects.filter(profile=auth_user.id)
        q2 = Quiz.objects.filter(course__in=q1)
        return q2.distinct()


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image'] # course

    def get_context_data(self, **kwargs):
        auth_user = self.request.user;
        context = super().get_context_data(**kwargs)
        context['course_form'] = ChooseCourseForm(auth_user)
        return context

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
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = QuizFilter(self.request.GET, queryset=self.get_queryset())
    #     return context

    def get_queryset(self):
        auth_user = self.request.user;

        # SubQueries - https://stackoverflow.com/questions/8556297/how-to-subquery-in-queryset-in-django
        q1 = Course.objects.filter(profile=auth_user.id)
        q2 = Quiz.objects.filter(course__in=q1)
        return q2.order_by('-date_created').distinct()


class UserQuizListView(ListView):
    model = Quiz
    template_name = 'quiz/user_quiz.html'   # <app>/<model>_<viewtype>.html
    context_object_name = 'quizzes'
    ordering = ['-date_created']            # - to inverse ordering
    # paginate_by = 3                         # number of quizzes per page

    def get_queryset(self):
        auth_user = self.request.user;
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        # SubQueries - https://stackoverflow.com/questions/8556297/how-to-subquery-in-queryset-in-django
        q1 = Course.objects.filter(profile=auth_user.id)
        q2 = Quiz.objects.filter(author=user).filter(course__in=q1)

        return q2.order_by('-date_created').distinct()
        


class QuizEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    fields = ['question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image'] # course

    def get_context_data(self, **kwargs):
        auth_user = self.request.user;
        context = super().get_context_data(**kwargs)
        context['course_form'] = ChooseCourseForm(auth_user)
        return context

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


@login_required
def quiz_upload(request):
    template = 'quiz/quiz_upload.html'
    auth_user = request.user
    form = QuizUploadForm(auth_user)

    if request.method == "POST":
        quiz_resource = QuizResource()
        dataset = Dataset()
        json_file = request.FILES['file']

        imported_data = dataset.load(json_file.read())
        print( imported_data )
        result = quiz_resource.import_data(dataset, dry_run=True)   # Test the data import

        if not result.has_errors():
            quiz_resource.import_data(dataset, dry_run=False)       # Actually import now

    context = {
        'form': form,
    }

    return render(request, template, context)


@csrf_exempt
@require_http_methods(["POST"])
def start_quiz(request, *args, **kwargs):
    # Convert from JSON to PYTHON: json.loads(x)
    # Convert from PYTHON to JSON: json.dumps(x)

    #* Reset 'Answer' model
    Answer.objects.all().delete()

    #* Get quiz object
    body = request.body.decode('utf-8')
    m = re.search('id=(.+?)&', body)
    if m:
        quiz_id = m.group(1)
    print(quiz_id)

    quiz = get_object_or_404(Quiz, id=quiz_id)

    #* Update quiz.start_date
    quiz.start_date = datetime.datetime.now()
    quiz.save()


    # #? Get 'quiz.id'
    # print("######################################################################")
    # print("request.body:")
    # print(request.body)

    # print("request.body.decode('utf-8'):")
    # print(request.body.decode('utf-8'))

    # s = '{"id": "7", "start_date": "2019-03-18 17:45:23", "right_ans": "A"}'
    # json_data = json.loads(s)
    # print("How it should be:")
    # print(json_data)
    # print("######################################################################")

    #? Abade:
    # json_data = json.loads(request.body)
    # print(json_data.quiz_id)

    to_return = {'type': 'success', 'msg': 'done', 'code': 200}
    return HttpResponse(json.dumps(to_return), content_type='application/json')


# Respostas vindas do microcontrolador
@csrf_exempt
@require_http_methods(["POST"])
def receive_response(request):
    date_now = datetime.datetime.now()

    json_data = json.loads(request.body)


import re   # for Start Quiz
from tablib import Dataset  # for Quiz Upload
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum

from users.forms import ProfileQuizForm
from .models import Quiz, Answer, Results, AnswerProcessing, Student, Terminal, Session, Lesson, LessonStudent
from .forms import QuizForm, QuizUploadForm
from .filters import QuizFilter
from users.models import Course, ProfileCourse, Profile #, Session
from .resources import QuizResource
from datetime import datetime

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
    fields = ['course', 'title', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image']

    def get_context_data(self, **kwargs):
        auth_user = self.request.user;
        context = super().get_context_data(**kwargs)
        context['course_form'] = QuizForm(auth_user)
        return context

    def form_valid(self, course_form):
        course_form.instance.author = self.request.user
        course_form.save()
        messages.add_message(self.request, messages.INFO, 'Your Quiz has been successfully created.')
        return super().form_valid(course_form)


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'quizzes'
    ordering = ['-date_created']        # - to inverse ordering
    # paginate_by = 3                     # number of quizzes per page

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
    fields = ['course', 'title', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image', 'anonymous']

    def get_context_data(self, **kwargs):

        auth_user = self.request.user;
        initial_data = {
            'course': [i.id for i in self.object.course.all()],
            'title': self.object.title,
            'question': self.object.question,
            'ansA': self.object.ansA,
            'ansB': self.object.ansB,
            'ansC': self.object.ansC,
            'ansD': self.object.ansD,
            'ansE': self.object.ansE,
            'right_ans': self.object.right_ans,
            'duration': self.object.duration,
            'image': self.object.image,
            'anonymous': self.object.anonymous

        }
        context = super().get_context_data(**kwargs)
        context['course_form'] = QuizForm(auth_user, initial = initial_data)
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


@csrf_exempt
@require_http_methods(["POST"])
def start_quiz(request, *args, **kwargs):

    print("QUIZ STARTED")

    # Reset 'Answer' and 'AnswerProcessing' models
    Answer.objects.all().delete()
    AnswerProcessing.objects.all().delete()

    # Get quiz object
    body = request.body.decode('utf-8')
    m = re.search('id=(.+?)&', body)
    if m:
        quiz_id = m.group(1)

    # Update quiz.start_date
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.start_date = datetime.datetime.now()
    quiz.save()
    print(quiz.id)
    print(quiz.start_date)

    to_return = {'type': 'success', 'msg': 'done', 'code': 200}
    return HttpResponse(json.dumps(to_return), content_type='application/json')


@csrf_exempt
@require_http_methods(["POST"])
def stop_quiz(request, *args, **kwargs):
    
    print("QUIZ ENDED")

    # Copy Answer to AnswerProcessing
    answers = Answer.objects.all().order_by('id')
    for answer in answers:
        try:
            student = Student.objects.get(uid=answer.uid)
            mac_id = Terminal.objects.get(mac=answer.mac)
            copy = AnswerProcessing(nmec=student.nmec, mac=mac_id, ans=answer.ans, date_time=answer.date_time)   #nmec=answer.nmec, mac=answer.mac
            copy.save()
        except Student.DoesNotExist:
            pass
        except Terminal.DoesNotExist:
            pass
        

    # Reset 'Answer' model
    Answer.objects.all().delete()

    # Get quiz object
    body = request.body.decode('utf-8')
    m = re.search('id=(.+?)&', body)
    if m:
        quiz_id = m.group(1)
    print(quiz_id)

    # Get quiz.start_date
    quiz = get_object_or_404(Quiz, id=quiz_id)
    print(quiz.start_date)

    # Create Session
    lesson = Lesson.objects.filter(user=quiz.author).latest('id')
    session = Session(quiz=quiz, lesson=lesson)
    session.save()

    # Check valid_ans (from 'Lesson')
    profile = get_object_or_404(Profile, user_id=quiz.author)
    print(lesson.valid_ans)
 
    # Anonymous = TRUE
    if quiz.anonymous == "Yes":
        print("ANONYMOUS QUIZ")
        # Deletes ALL but the first answer from each MAC
        lastSeenMAC = float('-Inf')
        if lesson.valid_ans == "Last":
            answers_processing = AnswerProcessing.objects.all().order_by('-id')
        else:
            answers_processing = AnswerProcessing.objects.all().order_by('id')
        for answer in answers_processing:
            if answer.mac == lastSeenMAC:
                answer.delete()
            else:
                lastSeenMAC = answer.mac

    # Anonymous = FALSE
    if quiz.anonymous == "No":
        print("NOT anonymous")
        # Check 'nmec + mac' on every object of 'AnswerProcessing' model
        # Deletes ALL but the last/first answer from each NMEC (based on 'valid_ans' from 'Lesson')
        lastSeenNMEC = float('-Inf')
        if lesson.valid_ans == "Last":
            answers_processing_inverse = AnswerProcessing.objects.all().order_by('-id')
        else:
            answers_processing_inverse = AnswerProcessing.objects.all().order_by('id')

        for answer in answers_processing_inverse:
            if answer.nmec == "00000":
                answer.delete()
            elif answer.nmec == lastSeenNMEC:
                answer.delete()     # We've seen this MAC in a previous row
            else:                   # New id found, save it and check future rows for duplicates.
                lastSeenNMEC = answer.nmec

        # Deletes ALL but the first answer from each MAC
        lastSeenMAC = float('-Inf')
        answers_processing = AnswerProcessing.objects.all().order_by('id')
        for answer in answers_processing:
            if answer.mac == lastSeenMAC:
                answer.delete()
            else:
                lastSeenMAC = answer.mac

    # Compare time-AnswerProcessing with time-Quiz and save to 'Results'
    answers_processed = AnswerProcessing.objects.all().order_by('id')

    for answer in answers_processed:
        # Time
        answer_time = answer.date_time - quiz.start_date
        print(answer.date_time)
        seconds = answer_time.total_seconds()
        print(seconds)
        float_sec = float(seconds)
        # Answer
        if answer.ans == quiz.right_ans: # and float_sec <= quiz.duration:
            evaluation = "right"
        else:
            evaluation = "wrong"
        print(evaluation)
        # Save Results
        if quiz.anonymous == "No":
            result = Results(quiz_id=Quiz.objects.get(id=quiz_id), student=answer.nmec, mac_address=answer.mac, answer=answer.ans, time=seconds, evaluation=evaluation, session=session, anonymous="No")
            if evaluation == "right":
                lesson_student = LessonStudent(lesson=lesson, course=quiz.course.last(), student=answer.nmec, right_ans=1, wrong_ans=0)
            else:
                lesson_student = LessonStudent(lesson=lesson, course=quiz.course.last(), student=answer.nmec, right_ans=0, wrong_ans=1)
        else:
            result = Results(quiz_id=Quiz.objects.get(id=quiz_id), student="00000", mac_address=answer.mac, answer=answer.ans, time=seconds, evaluation=evaluation, session=session, anonymous="Yes")
        result.save()
        lesson_student.save()

    # LessonStudent
    lesson_id = lesson
    lesson_answers = LessonStudent.objects.filter(lesson=lesson_id).order_by('student')
    print("Lesson Answers:")
    print(lesson_answers)

    student_nmec = float('-Inf')
    for ans in lesson_answers:
        
        right_answer = LessonStudent.objects.filter(lesson=lesson_id).filter(student=ans.student).aggregate(Sum('right_ans'))
        wrong_answer = LessonStudent.objects.filter(lesson=lesson_id).filter(student=ans.student).aggregate(Sum('wrong_ans'))
        print("Number of right answers:")
        total_right_ans=right_answer.get('right_ans__sum')  
        print(total_right_ans) 
        print("Number of wrong answers:")
        total_wrong_ans=wrong_answer.get('wrong_ans__sum')
        print(total_wrong_ans) 

        if ans.student == student_nmec:
            pass
        else:
            student_nmec = ans.student
            student_score = LessonStudent(lesson=ans.lesson, course = ans.course, student=ans.student, right_ans=0, wrong_ans=0, total_right=total_right_ans, total_wrong=total_wrong_ans)
            student_score.save()

    # Reset 'AnswerProcessing' model
    AnswerProcessing.objects.all().delete()

    to_return = {'type': 'success', 'msg': 'done', 'code': 200}
    return HttpResponse(json.dumps(to_return), content_type='application/json')


class ResultsListView(ListView):
    model = Results                # AnswerProcessing OR Results
    template_name = 'quiz/results.html' 
    context_object_name = 'answers'
    ordering = ['-date_time']  

    def get_queryset(self):
        auth_user = self.request.user;
        session_id = self.kwargs['session']

        # SubQueries - https://stackoverflow.com/questions/8556297/how-to-subquery-in-queryset-in-django
        q1 = Quiz.objects.filter(author=auth_user.id)
        q2 = Results.objects.filter(quiz_id_id__in=q1).filter(session_id=session_id)

        return q2.order_by('-date_time')


class SessionsListView(ListView):
    model = Session
    template_name = 'quiz/sessions.html'   # <app>/<model>_<viewtype>.html
    context_object_name = 'sessions'
    ordering = ['-date_created']            # - to inverse ordering

    def get_queryset(self):
        auth_user = self.request.user;

        # SubQueries - https://stackoverflow.com/questions/8556297/how-to-subquery-in-queryset-in-django
        q2 = Quiz.objects.filter(author=auth_user)
        q3 = Session.objects.filter(quiz_id__in=q2)

        return q3.order_by('-date_created').distinct()
        
        
@csrf_exempt
@require_http_methods(["POST"])
def quiz_response(request, *args, **kwargs):

    print("RESPONSE VIEW")

    # Get quiz object
    body = request.body.decode('utf-8')
    print(body)
    m = re.search('uid: (.+?),', body)
    if m:
        card_id = m.group(1)
        print(card_id)
    m = re.search('mac: (.+?),', body)
    if m:
        mac_id = m.group(1)
        print(mac_id)
    m = re.search('ans: (.+?)}', body)
    if m:
        ans = m.group(1)
        print(ans)

    answer = Answer(uid=card_id, mac=mac_id, ans=ans, date_time=datetime.datetime.now())
    answer.save()

    to_return = {'type': 'success', 'msg': 'done', 'code': 200}
    return HttpResponse(json.dumps(to_return), content_type='application/json')


@csrf_exempt
@require_http_methods(["POST"])
def new_lesson(request, *args, **kwargs):

    print("NEW LESSON STARTED")

    auth_user = request.user;
    user_lessons = Lesson.objects.filter(user=auth_user)
    print(user_lessons)

    try:
        lesson_id = user_lessons.order_by("-id")[0]
    except user_lessons.DoesNotExist:
        lesson_id = None

    lesson = get_object_or_404(Lesson, id=lesson_id.id)

    print(lesson.course.filter(lesson=lesson_id).last())

    to_return = {'type': 'success', 'course': str(lesson.course.filter(lesson=lesson_id).last()), 'id': lesson.id, 'code': 200}
    return HttpResponse(json.dumps(to_return), content_type='application/json')


@csrf_exempt
@require_http_methods(["POST"])
def get_quiz_course(request, *args, **kwargs):
    
    quiz_id = 0

    # Get quiz object
    body = request.body.decode('utf-8')
    m = re.search('id=(.+?)&', body)
    if m:
        quiz_id = m.group(1)

    # Update quiz.start_date
    quiz = get_object_or_404(Quiz, id=quiz_id)

    print("printing quiz_course")
    print(quiz.course.filter(quiz=quiz_id).last())

    to_return = {'type': 'success',  'quiz_course': str(quiz.course.filter(quiz=quiz_id).last()), 'code': 200}
    return HttpResponse(json.dumps(to_return), content_type='application/json')


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    fields = ['course', 'valid_ans']
    success_url = '/'

    def get_context_data(self, **kwargs):
        auth_user = self.request.user;
        context = super().get_context_data(**kwargs)
        context['lesson_form'] = ProfileQuizForm(auth_user)
        return context

    def form_valid(self, lesson_form):
        lesson_form.instance.user = self.request.user
        lesson_form.save()
        messages.add_message(self.request, messages.INFO, 'You have started a new Lesson.')
        print("aqui")
        return super().form_valid(lesson_form)
        #redirect('/')


class LessonsListView(ListView):
    model = Lesson
    template_name = 'quiz/lessons.html'   # <app>/<model>_<viewtype>.html
    context_object_name = 'lessons'
    ordering = ['-date_created']            # - to inverse ordering

    def get_queryset(self):
        auth_user = self.request.user;

        return Lesson.objects.filter(user=auth_user)


class LessonResultsListView(ListView):
    model = LessonStudent #Results  
    template_name = 'quiz/lesson_results.html' 
    context_object_name = 'answers'
    ordering = ['student']  

    def get_queryset(self):
        auth_user = self.request.user;
        #session_id = self.kwargs['session']
        lesson_id = self.kwargs['lesson']
        
        lesson_answers = LessonStudent.objects.filter(lesson=lesson_id).order_by('student', '-id')#.order_by('-id')
        print("Lesson Answers:")
        print(lesson_answers)

        #for lesson in lesson_answers:
            #print(session.id)
            #print(session.quiz.id)

        

        q1 = Quiz.objects.filter(author=auth_user.id)
        #q2 = Results.objects.filter(quiz_id_id__in=q1).filter(session_id=session_id)

        #print(sessions)
        #print(q2)
        #print(q2)

        return lesson_answers
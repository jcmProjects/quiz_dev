from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import QuizCreateView, QuizDetailView, UserQuizListView, QuizListView, QuizEditView, QuizDeleteView, start_quiz, stop_quiz, ResultsListView, SessionsListView, quiz_response, new_lesson, LessonCreateView, get_quiz_course, LessonsListView, LessonResultsListView
from . import views


urlpatterns = [
    path('', login_required(QuizListView.as_view()), name='quiz-home'),
    path('quiz/<str:username>', login_required(UserQuizListView.as_view()), name='user-quiz'),
    path('quiz/<int:pk>/', login_required(QuizDetailView.as_view()), name='quiz-detail'),
    path('quiz/new/', login_required(QuizCreateView.as_view()), name='quiz-create'),
    path('quiz/<int:pk>/edit/', login_required(QuizEditView.as_view()), name='quiz-edit'),
    path('quiz/<int:pk>/delete/', login_required(QuizDeleteView.as_view()), name='quiz-delete'),
    path('quiz/<int:pk>/start_quiz/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:pk>/stop_quiz/', views.stop_quiz, name='stop_quiz'),
    path('quiz/results/<int:session>/', ResultsListView.as_view(), name='quiz-results'),
    path('quiz/results/', SessionsListView.as_view(), name='quiz-sessions'),
    path('quiz/response/', views.quiz_response, name='quiz_response'),
    path('quiz/new_lesson/', views.new_lesson, name='new_lesson'),
    path('quiz/get_quiz_course/', views.get_quiz_course, name='get_quiz_course'),
    path('quiz/lesson/new/', login_required(LessonCreateView.as_view()), name='lesson-create'),
    path('quiz/lessons/', LessonsListView.as_view(), name='quiz-lessons'),
    path('quiz/lessons/<int:lesson>/', LessonResultsListView.as_view(), name='lesson-results'),
]

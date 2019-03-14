from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import QuizCreateView, QuizDetailView, UserQuizListView, QuizListView, QuizEditView, QuizDeleteView, QuizShowView
from . import views

urlpatterns = [
    path('', login_required(QuizListView.as_view()), name='quiz-home'),
    path('quiz/<str:username>', login_required(UserQuizListView.as_view()), name='user-quiz'),
    path('quiz/<int:pk>/', login_required(QuizDetailView.as_view()), name='quiz-detail'),
    path('quiz/<int:pk>/show/', login_required(QuizShowView.as_view()), name='quiz-show'),
    path('quiz/new/', login_required(QuizCreateView.as_view()), name='quiz-create'),
    path('quiz/<int:pk>/edit/', login_required(QuizEditView.as_view()), name='quiz-edit'),
    path('quiz/<int:pk>/delete/', login_required(QuizDeleteView.as_view()), name='quiz-delete'),
]

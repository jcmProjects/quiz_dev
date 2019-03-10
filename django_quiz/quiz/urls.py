from django.urls import path
from .views import QuizCreateView, QuizDetailView, UserQuizListView, QuizListView, QuizEditView, QuizDeleteView
from . import views

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz-home'),
    path('quiz/<str:username>', UserQuizListView.as_view(), name='user-quiz'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/new/', QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/edit/', QuizEditView.as_view(), name='quiz-edit'),
    path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz-delete'),
    # path('about/', views.about, name='blog-about'),
]
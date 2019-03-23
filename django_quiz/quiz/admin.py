from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Quiz, Answer, Results, AnswerProcessing

# admin.site.register(Quiz)
@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Results)

admin.site.register(Answer)

admin.site.register(AnswerProcessing)

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Quiz, Answer, Results, AnswerProcessing, Student, Terminal, Session

# admin.site.register(Quiz)
@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    pass


#admin.site.register(Results)
@admin.register(Results)
class QuizAdmin(ImportExportModelAdmin):
    pass


@admin.register(Student)
class QuizAdmin(ImportExportModelAdmin):
    pass


@admin.register(Terminal)
class QuizAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Answer)
admin.site.register(AnswerProcessing)
admin.site.register(Session)


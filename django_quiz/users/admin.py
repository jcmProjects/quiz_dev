from django.contrib import admin
from .models import Profile, Course, ProfileCourse, Session


admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(ProfileCourse)
admin.site.register(Session)

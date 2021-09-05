from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Course, Subject, LeaveStudentReport
# Register your models here.


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(LeaveStudentReport)

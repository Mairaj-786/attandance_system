from django.urls import path
from .views import *

urlpatterns = [
    path('', do_login, name="login"),
    path('logout', do_logout, name="logout"),
    # Admin dashboard
    path('admin-dashboard', admin_dash, name="admin_dashboard"),
    path('admin-profile', admin_profile, name="admin_profile"),
    path('add-student', add_student, name="add_student"),
    path('admin-edit-students/<int:id>',
         admin_edit_students, name="admin_edit_students"),
    path('leave', manage_leave, name="manage_leave"),
    path('manage-leave/<int:id>',
         leave_approve_or_reject, name="approve_or_reject"),

    # students urls
    path('student-dashboard', student_dash, name="student_dashboard"),
    path('student-profile', student_profile, name="student_profile"),
    path('add-course', add_course, name="add_course"),
    path('student-leave', student_leave, name="student_leave"),
]

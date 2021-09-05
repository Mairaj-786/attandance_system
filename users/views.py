from django.contrib.auth import login, logout
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from users.EmailBackEnd import EmailBackEnd
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .models import CustomUser, Student, Course, Subject, LeaveStudentReport
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm, CourseForm, ProfileUpdateFormAdmin, LeaveStudentReportForm, LeaveStudentReportAdminForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# Create your views here.


def admin_dash(request):
    if request.user.is_authenticated:
        if request.user.user_type == "1":
            return render(request, 'admin_home.html')
        else:
            return HttpResponse("only admin access")
    else:
        return redirect('/')


def student_dash(request):
    if request.user.is_authenticated:
        if request.user.user_type == "2":
            return render(request, 'student_home.html')
        else:
            return HttpResponse("Student Access only")
    else:
        return redirect('/')


def student_profile(request):
    if request.user.user_type == "2":
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.student)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your Account has been updated!')
                return redirect('student_profile')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.student)

            context = {
                'u_form': u_form,
                'p_form': p_form
            }
            return render(request, 'student_profile.html', context)


def admin_profile(request):
    if request.user.user_type == "1":
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateFormAdmin(
                request.POST, request.FILES, instance=request.user.adminhod)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your Account has been updated!')
                return redirect('admin_profile')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateFormAdmin(instance=request.user.adminhod)

            context = {
                'u_form': u_form,
                'p_form': p_form
            }
            return render(request, 'admin_profile.html', context)


def do_logout(request):
    logout(request)
    return redirect('/')


def do_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == "2":
            return redirect('/student-dashboard')
        else:
            return redirect('/admin-dashboard')
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return redirect("admin_dashboard")
            elif user.user_type == "2":
                return redirect("student_dashboard")
            else:
                return HttpResponse("Invalid User")
        else:
            messages.info(request, 'Invalid crediontal')
    return render(request, 'login.html')


def add_student(request):
    if request.user.user_type != '1':
        return HttpResponse('admin access')
    else:
        if request.method == "POST":
            username = request.POST['username']
            first_name = request.POST['first_name']
            email = request.POST['email']
            password = request.POST['password']
            address = request.POST['address']

            if username == '' and first_name == '' and email == '' and password == '' and address == '':
                messages.error(request, 'all fields are required')
                return redirect('/add-student')
            else:
                user = CustomUser.objects.create_user(username=username, first_name=first_name,
                                                      email=email, password=password, user_type=2)
                user.student.address = address
                user.save()
                messages.success(request, 'Account Created for ' + first_name)
                return redirect('add_student')
    students = Student.objects.all()
    return render(request, 'admin_add_student.html', {'students': students})


def add_course(request):
    if request.user.user_type != '1':
        return HttpResponse('admin access')
    else:
        if request.method == "POST":
            ad_course = CourseForm(request.POST)
            if ad_course.is_valid():
                course_name = ad_course.cleaned_data['course_name']
                ad_course.save()
                messages.info(request, f"{course_name} addedd successfully")
                return redirect('add_course')
        else:
            ad_course = CourseForm()
            courses = Course.objects.all()
        return render(request, 'add_course.html', {'ad_course': ad_course, "courses": courses})


def admin_edit_students(request, id=None):
    if request.method == "POST":
        student = get_object_or_404(Student, pk=id)
        p_form = ProfileUpdateForm(request.POST, instance=student)
        u_form = UserUpdateForm(request.POST, instance=student.admin)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            return HttpResponseRedirect('/add-student')
    else:
        u_form = UserUpdateForm()
        p_form = ProfileUpdateForm()

        context = {
            "p_form": p_form,
            "u_form": u_form,
        }
    return render(request, 'admin_edit_student.html', context)


def student_leave(request):
    if request.method == "POST":
        leave_form = LeaveStudentReportForm(request.POST)
        if leave_form.is_valid():
            instance = leave_form.save(commit=False)
            instance.student_id = request.user.student
            instance.save()
            messages.success(request, 'Leave Applied success')
            return HttpResponseRedirect('student-leave')
    else:
        leave_form = LeaveStudentReportForm()
        student_obj = Student.objects.get(admin=request.user.id)
        leave_date = LeaveStudentReport.objects.filter(student_id=student_obj)

    return render(request, 'student_leave.html', {'leave_form': leave_form, 'leave_date': leave_date})


def manage_leave(request):
    student_leave = LeaveStudentReport.objects.all()
    return render(request, 'admin_leave.html', {'student_leave': student_leave})


def leave_approve_or_reject(request, id=None):
    manage_leave = LeaveStudentReport.objects.get(id=id)
    if request.method == "POST":
        lsaform = LeaveStudentReportAdminForm(
            request.POST, instance=manage_leave)
        if lsaform.is_valid():
            insatance = lsaform.save(commit=False)
            insatance.student_id = manage_leave.student_id
            insatance.save()
            return HttpResponseRedirect('/leave')
    else:
        lsaform = LeaveStudentReportAdminForm()
    context = {
        'manage_leave': manage_leave,
        'lsaform': lsaform,
    }
    return render(request, 'admin_manage_leave.html', context)

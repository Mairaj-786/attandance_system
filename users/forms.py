from django import forms
from django.db import models
from django.db.models import fields
from .models import AdminHOD, CustomUser, Student, Course, LeaveStudentReport
from django.contrib.auth.forms import AuthenticationForm


class LeaveStudentReportForm(forms.ModelForm):
    leave_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'date', 'placeholder': "leave_date"}))
    leave_message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': "leave_message"}))

    class Meta:
        model = LeaveStudentReport
        fields = ['leave_date', 'leave_message']


class LeaveStudentReportAdminForm(forms.ModelForm):

    class Meta:
        model = LeaveStudentReport
        fields = ['status']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Password"}))

    class Meta:
        model = CustomUser
        field = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username"}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Email"}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProfileUpdateFormAdmin(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': "Address"}))

    class Meta:
        model = AdminHOD
        fields = ['address', 'profile_pic']


class ProfileUpdateForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': "Address"}))

    class Meta:
        model = Student
        fields = ['address', 'gender', 'course', 'profile_pic']


class CourseForm(forms.ModelForm):
    course_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Course
        fields = ['course_name']

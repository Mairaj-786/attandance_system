from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomUser(AbstractUser):
    user_tyepe_data = (
        (1, "HOD"),
        (2, "Student"),
    )
    user_type = models.CharField(
        default=1, choices=user_tyepe_data, max_length=10)


Gender_choices = [
    ("Male", "Male"),
    ("Female", "Female")
]


class AdminHOD(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        default="default.jpg", upload_to="profile_pics")

    objects = models.Manager()

    def __str__(self):
        return self.admin.username


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.course_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    admin_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.subject_name} is subject of {self.admin_id.admin.username}"


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(
        default="Male", choices=Gender_choices, max_length=6)
    profile_pic = models.ImageField(
        default="default.jpg", upload_to="profile_pics")
    course = models.ForeignKey(
        Course, on_delete=models.DO_NOTHING, default=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name + " - Profile"


class Attandance(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attandance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class AttandanceReport(models.Model):
    subject_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attandance_id = models.ForeignKey(Attandance, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


leave_status = [
    ("Aprove", "Aprove"),
    ("Reject", "Reject"),
    ("Panding", "Panding")
]


class LeaveStudentReport(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    leave_date = models.CharField(max_length=200)
    leave_message = models.TextField()
    status = models.CharField(
        default='Panding', choices=leave_status, max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def studet_leaves(self):
        return self.leavestudentreport_set.all()

    def __str__(self):
        return f"Leave for {self.leave_message} by {self.student_id.admin.username}"


class FeedbackStudent(models.Model):
    subject_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    leave_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Student.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.student.save()

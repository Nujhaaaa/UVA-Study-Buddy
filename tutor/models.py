from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=self.normalize_email(
            email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class user(AbstractBaseUser, PermissionsMixin):
    is_tutor = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    id = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=50, null=True, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'email']

    def __str__(self):
        return self.email


class TutorCourse(models.Model):
    tutor = models.ForeignKey(user, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    course_name = models.CharField(max_length=255)
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    available_time_frames = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course} - {self.course_name}"


class Session(models.Model):
    student = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='student_sessions')
    tutor = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='tutor_sessions')
    course = models.ForeignKey(TutorCourse, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), (
        'accepted', 'Accepted'), ('declined', 'Declined')], default='pending')

    def __str__(self):
        return f"{self.student.email} - {self.tutor.email} - {self.course.course} - {self.status}"

class ThreadModel(models.Model):
  user = models.ForeignKey('user', on_delete=models.CASCADE, related_name='+')
  receiver = models.ForeignKey('user', on_delete=models.CASCADE, related_name='+')
  need_noti = models.BooleanField(default=False)
  has_unread = models.BooleanField(default=False)

class MessageModel(models.Model):
  thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
  sender_user = models.ForeignKey('user', on_delete=models.CASCADE, related_name='+')
  receiver_user = models.ForeignKey('user', on_delete=models.CASCADE, related_name='+')
  body = models.CharField(max_length=1000)
#   image = models.ImageField(upload_to='', blank=True, null=True)
  date = models.DateTimeField(default=timezone.now)
  is_read = models.BooleanField(default=False)
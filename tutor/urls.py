from django.urls import path

from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from tutor.views import ListThreads, CreateThread, ThreadView, CreateMessage

urlpatterns = [
    # setting path to homepage
    path('', TemplateView.as_view(template_name="index.html")),
    path('home/tutor/<int:id>/', views.tutor_logged_in, name="tutor_logged_in"),
    path('home/student/<int:id>', views.student_logged_in, name="student_logged_in"),
    path('tutor_calendar/', views.tutor_calendar, name='tutor_calendar'),
    path('student_calendar/', views.student_calendar, name='student_calendar'),
    path('createStudent/', views.createStudent, name="createStudent"),
    path('createTutor/', views.createTutor, name="createTutor"),
    path('login_check/', views.login_check, name="login_check"),
    path('signup/', views.sign_up, name="sign_up"),
    path('tutoring/', views.tutoring_page, name='tutoring_page'),
    path("login/", views.login, name="login"),
    path('home/student/<int:id>/sessions/', views.student_sessions, name="student_sessions"),
    path('home/tutor/<int:id>/sessions/', views.tutor_sessions, name="tutor_sessions"),
    path('home/student/messages/', ListThreads.as_view(), name="student_inbox"),
    path('home/tutor/messages/', ListThreads.as_view(), name="tutor_inbox"),
    path('home/tutor/create-thread', CreateThread.as_view(), name='create-thread'),
    path('home/student/create-thread', CreateThread.as_view(), name='create-thread'),
    path('home/tutor/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('home/student/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('home/tutor/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
    path('home/student/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
    path('add_course/<str:course_id>/', views.add_course, name='add_course'),
    path('tutor_courses/<int:id>/', views.tutor_courses, name='tutor_courses'),
    path('student/courses/<int:id>/', views.student_courses, name='student_courses'),
    path('logout', LogoutView.as_view()),
    path('create_session/<int:tutor_course_id>/',
         views.create_session, name='create_session'),
    path('update_session_status/<int:session_id>/',
         views.update_session_status, name='update_session_status'),

]
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from tutor.models import TutorCourse, Session
from .models import TutorCourse, user, ThreadModel, MessageModel
from django.db.models import Q
from django.contrib.auth import login as auth_login
from .sis_api import search_courses
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import TutorCourseForm, SessionForm
from django.views import View
from tutor.forms import MessageForm, ThreadForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def tutor_calendar(request):
    tutor = request.user
    sessions = request.user.tutor_sessions.all()
    selected_month = request.GET.get('month', date.today().month)
    selected_year = request.GET.get('year', date.today().year)
    sessions = sessions.filter(date__month=selected_month, date__year=selected_year)
    context = {'sessions': sessions, 'selected_month': selected_month, 'selected_year': selected_year}
    return render(request, 'tutor/tutor_calendar.html', context)

@login_required
def student_calendar(request):
    student = request.user
    sessions = request.user.student_sessions.all()
    selected_month = request.GET.get('month', date.today().month)
    selected_year = request.GET.get('year', date.today().year)
    sessions = sessions.filter(date__month=selected_month, date__year=selected_year)
    context = {'sessions': sessions, 'selected_month': selected_month, 'selected_year': selected_year}
    return render(request, 'tutor/student_calendar.html', context)



def index(request):
    return render(request, 'index.html')


@login_required
def student_logged_in(request, id):
    query = request.GET.get("q", "")
    courses = []
    if query:
        term = request.GET.get("term", "1232")
        courses = search_courses(query, term)

        for course in courses:
            course_id = f"{course['subject']}{course['catalog_nbr']}"
            tutors = TutorCourse.objects.filter(course=course_id)
            course['tutors'] = tutors
            course['tutor_count'] = tutors.count()

    form = SessionForm()

    return render(request, "student_logged_in.html", {
        "query": query,
        "courses": courses,
        "form": form
    })

@login_required
def tutor_logged_in(request, id):
    query = request.GET.get("q", "")
    courses = []
    if query:
        term = request.GET.get("term", "1232")
        courses = search_courses(query, term)

    return render(request, "tutor_logged_in.html", {
        "query": query,
        "courses": courses,
    })


@login_required
def create_session(request, tutor_course_id):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            tutor_course = TutorCourse.objects.get(pk=tutor_course_id)
            tutor = tutor_course.tutor
            student = request.user

            # Get the session time from the form data
            session_time = form.cleaned_data['session_time']

            # Create a new Session instance with hourly_rate and the provided session time
            session = Session(student=student, tutor=tutor, course=tutor_course,
                              hourly_rate=tutor_course.hourly_rate, time=session_time)
            session.save()

            # Redirect to the student's sessions tab
            return redirect('student_sessions', id=student.id)
    else:
        return redirect('student_logged_in', id=request.user.id)


def createStudent(request):
    request.session['user_type'] = 'student'
    request.session.modified = True
    return HttpResponseRedirect('/accounts/google/login/')


def createTutor(request):
    request.session['user_type'] = 'tutor'
    request.session.modified = True
    return HttpResponseRedirect('/accounts/google/login/')


@login_required
def add_course(request, course_id):
    tutor = request.user

    if request.method == 'POST':
        form = TutorCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = tutor
            course.course = course_id
            course.save()
            return redirect('tutor_logged_in', id=tutor.id)
    else:
        form = TutorCourseForm()
    return render(request, 'add_course.html', {'form': form, 'course_id': course_id})


def update_session_status(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "accept":
            session.status = "accepted"
        elif action == "decline":
            session.status = "declined"

        session.save()
        return redirect("tutor_sessions", id=request.user.id)

    # If request method is not POST, redirect to the tutor_sessions view
    return redirect("tutor_sessions", id=request.user.id)


def sign_up(request):
    return render(request, 'sign_up.html')


def login(request):
    return render(request, 'login.html')


def user_type_selection(request):
    return render(request, 'user_type_selection.html')


def login_check(request):
    if request.user.is_authenticated:
        if user.objects.filter(email=request.user.email).exists():
            cur_user = user.objects.get(email=request.user.email)
            auth_login(request, cur_user)  # Log the user in
            if (cur_user.user_type == "student"):
                return redirect('student_logged_in', id=cur_user.id)
            else:
                return redirect('tutor_logged_in', id=cur_user.id)
        else:
            return redirect('sign_up')
    else:
        return redirect('login')


def tutoring_page(request):
    return render(request, 'tutor/tutoring.html')


def student_sessions(request, id):
    sessions = request.user.student_sessions.all()
    return render(request, 'student_sessions.html', {'sessions': sessions})


def tutor_sessions(request, id):
    sessions = request.user.tutor_sessions.all()
    return render(request, 'tutor_sessions.html', {'sessions': sessions})

@login_required
def student_courses(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    if request.user not in course.students.all():
        messages.warning(request, "You do not have permission to view this course.")
        return redirect("home")
    context = {"course": course}
    return render(request, "student_courses.html", context)

def tutor_courses(request, id):
    tutor_courses = TutorCourse.objects.filter(tutor=request.user)
    return render(request, 'courses.html', {'courses': tutor_courses})

class CreateThread(View):
  def get(self, request, *args, **kwargs):
    form = ThreadForm()
    context = {
      'form': form
    }
    if user.objects.filter(email=request.user.email).exists():
        cur_user = user.objects.get(email=request.user.email)
        if (cur_user.user_type == "student"):
            return render(request, 'tutor_create_thread.html', context)
        else:
            return render(request, 'student_create_thread.html', context)
  def post(self, request, *args, **kwargs):
    form = ThreadForm(request.POST)
    email = request.POST.get('email')
    try:
      receiver = user.objects.get(email=email)
      if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
        thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
        return redirect('thread', pk=thread.pk)

      if request.user==user.objects.get(email=email):
          return redirect('create-thread')

      if form.is_valid():
        sender_thread = ThreadModel(
          user=request.user,
          receiver=receiver
        )
        sender_thread.save()
        thread_pk = sender_thread.pk
        return redirect('thread', pk=thread_pk)
    except:
      return redirect('create-thread')


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        for thread in threads:
            if thread.receiver == request.user:
                thread.receiver = thread.user
                thread.user = request.user
                thread.save()
        if request.user.user_type == "student":
            template = 'student_inbox.html'
        else:
            template = 'tutor_inbox.html'
        context = {
            'threads': threads
        }
        return render(request, template, context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
      thread = ThreadModel.objects.get(pk=pk)
      if thread.receiver == request.user:
          receiver = thread.user
          message = MessageModel(
             thread=thread,
             sender_user=request.user,
             receiver_user=receiver,
             body=request.POST.get('message'),
           )
          thread.need_noti=True
          thread.save()
          message.save()
      else:
          receiver = thread.receiver
          message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message'),
          )
          thread.need_noti=True
          thread.save()
          message.save()
      return redirect('thread', pk=pk)

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        thread.need_noti=False
        if(thread.receiver==request.user):
                thread.receiver = thread.user
                thread.user = request.user
        thread.save()
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
          'thread': thread,
          'form': form,
          'message_list': message_list
        }
        if user.objects.filter(email=request.user.email).exists():
            cur_user = user.objects.get(email=request.user.email)
            if (cur_user.user_type == "student"):
                return render(request, 'tutor_thread.html', context)
            else:
                return render(request, 'student_thread.html', context)

        # Redirect the user to the correct page after exiting messages
        if cur_user.user_type == "student":
            return redirect('student_logged_in', id=request.user.id)
        else:
            return redirect('tutor_logged_in', id=request.user.id)

       
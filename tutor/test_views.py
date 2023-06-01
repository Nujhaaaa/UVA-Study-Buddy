from django.test import TestCase
from django.urls import reverse
from .models import user, TutorCourse, Session, ThreadModel, MessageModel
from datetime import datetime, timedelta
from django.utils import timezone


class UserModelTests(TestCase):
    def setUp(self):
        self.tutor = user.objects.create_user(
            username='tutor',
            first_name='Tutor',
            last_name='Test',
            user_type='tutor',
            email='tutor@test.com',
            password='testpassword'
        )

        self.student = user.objects.create_user(
            username='student',
            first_name='Student',
            last_name='Test',
            user_type='student',
            email='student@test.com',
            password='testpassword'
        )

    def test_create_user(self):
        self.assertEqual(self.tutor.email, 'tutor@test.com')
        self.assertEqual(self.student.email, 'student@test.com')

    def test_create_superuser(self):
        admin = user.objects.create_superuser(
            username='admin',
            first_name='Admin',
            last_name='Test',
            user_type='admin',
            email='admin@test.com',
            password='testpassword'
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

class TutorCourseModelTests(TestCase):
    def setUp(self):
        self.tutor = user.objects.create_user(
            username='tutor',
            first_name='Tutor',
            last_name='Test',
            user_type='tutor',
            email='tutor@test.com',
            password='testpassword'
        )

        self.course = TutorCourse.objects.create(
            tutor=self.tutor,
            course='MATH101',
            course_name='Basic Math',
            hourly_rate=20.00,
            available_time_frames='Monday-Friday, 9am-5pm'
        )

    def test_course_creation(self):
        self.assertEqual(self.course.course, 'MATH101')
        self.assertEqual(self.course.course_name, 'Basic Math')

class SessionModelTests(TestCase):
    def setUp(self):
        self.tutor = user.objects.create_user(
            username='tutor',
            first_name='Tutor',
            last_name='Test',
            user_type='tutor',
            email='tutor@test.com',
            password='testpassword'
        )

        self.student = user.objects.create_user(
            username='student',
            first_name='Student',
            last_name='Test',
            user_type='student',
            email='student@test.com',
            password='testpassword'
        )

        self.course = TutorCourse.objects.create(
            tutor=self.tutor,
            course='MATH101',
            course_name='Basic Math',
            hourly_rate=20.00,
            available_time_frames='Monday-Friday, 9am-5pm'
        )

        self.session = Session.objects.create(
            student=self.student,
            tutor=self.tutor,
            course=self.course,
            hourly_rate=self.course.hourly_rate,
            time=datetime.now() + timedelta(days=1),
            status='pending'
        )

    def test_session_creation(self):
        self.assertEqual(self.session.status, 'pending')
        self.assertEqual(self.session.student.email, 'student@test.com')
        self.assertEqual(self.session.tutor.email, 'tutor@test.com')


class ThreadModelTests(TestCase):
    def setUp(self):
        self.user1 = user.objects.create_user(
            username='user1',
            first_name='User',
            last_name='One',
            user_type='student',
            email='user1@test.com',
            password='testpassword'
        )

        self.user2 = user.objects.create_user(
            username='user2',
            first_name='User',
            last_name='Two',
            user_type='student',
            email='user2@test.com',
            password='testpassword'
        )

        self.thread = ThreadModel.objects.create(
            user=self.user1,
            receiver=self.user2,
            need_noti=False,
            has_unread=False
        )

    def test_thread_creation(self):
        self.assertEqual(self.thread.user.email, 'user1@test.com')
        self.assertEqual(self.thread.receiver.email, 'user2@test.com')
        self.assertFalse(self.thread.need_noti)
        self.assertFalse(self.thread.has_unread)

class MessageModelTests(TestCase):
    def setUp(self):
        self.user1 = user.objects.create_user(
            username='user1',
            first_name='User',
            last_name='One',
            user_type='student',
            email='user1@test.com',
            password='testpassword'
        )

        self.user2 = user.objects.create_user(
            username='user2',
            first_name='User',
            last_name='Two',
            user_type='student',
            email='user2@test.com',
            password='testpassword'
        )

        self.thread = ThreadModel.objects.create(
            user=self.user1,
            receiver=self.user2,
            need_noti=False,
            has_unread=False
        )

        self.message = MessageModel.objects.create(
            thread=self.thread,
            sender_user=self.user1,
            receiver_user=self.user2,
            body="Hello, how are you?",
            date=timezone.now(),
            is_read=False
        )

    def test_message_creation(self):
        self.assertEqual(self.message.sender_user.email, 'user1@test.com')
        self.assertEqual(self.message.receiver_user.email, 'user2@test.com')
        self.assertEqual(self.message.body, "Hello, how are you?")
        self.assertFalse(self.message.is_read)

from django.test import TestCase
from tutor.models import user, TutorCourse, Session, ThreadModel, MessageModel


class TestModels(TestCase):   
    
    def setUp(self):
        self.student = user.objects.create(email="student@example.com", user_type="student", username="studentuser")
        self.tutor = user.objects.create(email="tutor@example.com", user_type="tutor", username="tutoruser")
        self.course = TutorCourse.objects.create(tutor=self.tutor, course="MATH101", course_name="Mathematics 101", hourly_rate=30, available_time_frames="9AM-12PM, 2PM-5PM")
        self.session = Session.objects.create(student=self.student, tutor=self.tutor, course=self.course, hourly_rate=30, time="2023-06-01T12:00:00Z")
        self.thread = ThreadModel.objects.create(user=self.student, receiver=self.tutor)
        self.message = MessageModel.objects.create(thread=self.thread, sender_user=self.student, receiver_user=self.tutor, body="Hello!")

    
    def test_user_model(self):
        self.assertEqual(self.student.email, "student@example.com")
        self.assertEqual(self.student.user_type, "student")

    def test_tutor_course_model(self):
        self.assertEqual(self.course.course, "MATH101")
        self.assertEqual(self.course.course_name, "Mathematics 101")
        self.assertEqual(self.course.hourly_rate, 30)

    def test_session_model(self):
        self.assertEqual(self.session.student, self.student)
        self.assertEqual(self.session.tutor, self.tutor)
        self.assertEqual(self.session.course, self.course)
        self.assertEqual(self.session.hourly_rate, 30)
        self.assertEqual(self.session.status, "pending")

    def test_thread_model(self):
        self.assertEqual(self.thread.user, self.student)
        self.assertEqual(self.thread.receiver, self.tutor)

    def test_message_model(self):
        self.assertEqual(self.message.thread, self.thread)
        self.assertEqual(self.message.sender_user, self.student)
        self.assertEqual(self.message.receiver_user, self.tutor)
        self.assertEqual(self.message.body, "Hello!")
        self.assertFalse(self.message.is_read)

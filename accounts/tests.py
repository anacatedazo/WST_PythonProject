from django.test import TestCase
from .models import Student

class StudentModelTest(TestCase):
    def test_create_student(self):
        student = Student.objects.create_user(
            student_id="2025-001",
            fullname="Ana Cate",
            section="BSIT 3A",
            age=21,
            email="ana@example.com",
            password="test123"
        )
        self.assertEqual(student.fullname, "Ana Cate")

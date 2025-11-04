from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class StudentManager(BaseUserManager):
    def create_user(self, student_id, fullname, section, age, email, password=None):
        if not email:
            raise ValueError("Students must have an email address")
        student = self.model(
            student_id=student_id,
            fullname=fullname,
            section=section,
            age=age,
            email=self.normalize_email(email),
        )
        student.set_password(password)
        student.save(using=self._db)
        return student


class Student(AbstractBaseUser):
    student_id = models.CharField(max_length=20, unique=True)
    fullname = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = StudentManager()

    USERNAME_FIELD = "student_id"
    REQUIRED_FIELDS = ["fullname", "email"]

    def __str__(self):
        return self.fullname

from django.db import models
from django.contrib.auth.models import User

class PreTest(models.Model):
    # Link each record to a student (user)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    # Account Information
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    date_of_pretest = models.DateField()

    # Physical Data
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    bmi = models.FloatField(blank=True, null=True)

    # Performance Data
    vo2_max = models.FloatField(blank=True, null=True)
    flexibility_cm = models.FloatField()
    strength_reps = models.FloatField()
    agility_sec = models.FloatField()
    speed_sec = models.FloatField()
    endurance_min = models.FloatField()

    def __str__(self):
        return f"{self.full_name} - Pre-Test"

    def calculate_bmi(self):
        """Automatic BMI computation"""
        if self.height_cm > 0:
            self.bmi = round(self.weight_kg / ((self.height_cm / 100) ** 2), 2)
        else:
            self.bmi = 0
        return self.bmi

    def calculate_vo2max(self):
        """Simple placeholder formula for demo (you can replace later)"""
        # Example formula (can be replaced with more scientific one)
        self.vo2_max = round(15.3 * (60 / self.speed_sec), 2) if self.speed_sec > 0 else 0
        return self.vo2_max

    def save(self, *args, **kwargs):
        self.calculate_bmi()
        self.calculate_vo2max()
        super().save(*args, **kwargs)


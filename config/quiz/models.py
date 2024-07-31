from django.db import models

class User(models.Model):
    APPLICANT = 'applicant'
    STUDENT = 'student'
    
    ROLE_CHOICES = [
        (APPLICANT, 'Applicant'),
        (STUDENT, 'Student'),
    ]

    id = models.BigAutoField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=100)
    age = models.PositiveIntegerField(verbose_name='Age')
    phone_number = models.CharField(verbose_name='Phone Number', max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=APPLICANT)
    # telegram_id = models.BigIntegerField(verbose_name='Telegram ID', unique=True, default=1)

    def __str__(self):
        return f"Applicant {self.id} ({self.get_role_display()})"

class ApplicantQuestion(models.Model):
    text = models.TextField(verbose_name='Question Applicant')

class ApplicantOption(models.Model):
    question = models.ForeignKey(ApplicantQuestion, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='Option Text')

    def __str__(self):
        return self.text

class Applicant(models.Model):
    id = models.BigIntegerField(verbose_name='Applicant ID', primary_key=True)
    selected_option = models.ForeignKey(ApplicantOption, related_name='applicants', on_delete=models.CASCADE)

    def __str__(self):
        return f"Applicant {self.id}"


class StudentQuestion(models.Model):
    text = models.TextField(verbose_name='Student Question')

class StudentOption(models.Model):
    question = models.ForeignKey(StudentQuestion, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='Option Text')

    def __str__(self):
        return self.text

class Student(models.Model):
    id = models.BigIntegerField(verbose_name='Student ID', primary_key=True)
    selected_option = models.ForeignKey(StudentOption, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return f"Student {self.id}"

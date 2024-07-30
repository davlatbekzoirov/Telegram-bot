# from django.contrib import admin
# from jazzmin.admin import UserAdmin, ModelAdminGroup
# from .models import User, ApplicantQuestion, ApplicantOption, Applicant, StudentQuestion, StudentOption, Student

# # Register your models here using Jazzmin's custom admin classes

# class ApplicantAdmin(ModelAdminGroup):
#     menu_label = 'Applicant'
#     items = (ApplicantQuestion, ApplicantOption, Applicant)

# class StudentAdmin(ModelAdminGroup):
#     menu_label = 'Student'
#     items = (StudentQuestion, StudentOption, Student)

# admin.site.register(User, UserAdmin)
# admin.site.register(ApplicantQuestion)
# admin.site.register(ApplicantOption)
# admin.site.register(Applicant, ApplicantAdmin)
# admin.site.register(StudentQuestion)
# admin.site.register(StudentOption)
# admin.site.register(Student, StudentAdmin)

from django.contrib import admin
from .models import User, ApplicantQuestion, ApplicantOption, Applicant, StudentQuestion, StudentOption, Student

admin.site.register(User)
admin.site.register(ApplicantQuestion)
admin.site.register(ApplicantOption)
admin.site.register(Applicant)
admin.site.register(StudentQuestion)
admin.site.register(StudentOption)
admin.site.register(Student)

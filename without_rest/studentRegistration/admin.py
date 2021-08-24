from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll_number', 'gender', "address"]


admin.site.register(Student, StudentAdmin)
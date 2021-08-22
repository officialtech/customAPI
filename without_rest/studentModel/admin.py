from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'roll_no', 'name', 'address', 'registration_no')

admin.site.register(Student, StudentAdmin)
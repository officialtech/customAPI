
from .views import StudentApi
from django.urls import path

urlpatterns = [
    path('student/', StudentApi.as_view(), name="student_api"),
]

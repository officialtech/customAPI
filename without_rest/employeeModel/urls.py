from django.urls import path
from . import views

urlpatterns = [
    path('student/<int:id>/', views.StudentView.as_view(), name="one_student_data"),
    path('student-detail/<int:id>', views.StudentDetailSerializeView.as_view(), name="all_student_data"),
    path('students/', views.StudentListSerializeView.as_view(), name="list_of_students"),
    path('post/', views.StudentSerializePostView.as_view(), name="post_request"),
    path('student-data/', views.StudentApiView.as_view(), name="student_api"),    # one and only one api for all
]

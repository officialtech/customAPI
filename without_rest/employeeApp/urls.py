from django.urls import path
from . import views

urlpatterns = [
    path('html/', views.employeeDataView),
    path('json/', views.employeeDataJsonView),
    path('django/', views.employeeDataDjangoJsonView),
    path('class/', views.JSONdata.as_view(), name="class_based_view"),
    path('mixins/', views.JsonDataWithMixinView.as_view(), name="using_mixins"),
]

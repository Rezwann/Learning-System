from django.urls import path

from Main import views

urlpatterns = [
    path('', views.get_subjects)
]

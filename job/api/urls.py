from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.register),
    path('login/',views.login),
    path('post/',views.newjob),
    path('apply/',views.applicant)    
]

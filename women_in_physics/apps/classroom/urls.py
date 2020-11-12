from django.urls import path

from . import views

app_name = 'classroom'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('classroom/', views.classroom, name='classroom'),
    path('response/', views.response, name='response'),
    path('changestatus/<slug:post>/', views.changestatus, name='changestatus'),
    path('reset/student/', views.reset_student, name='reset_student'),
]
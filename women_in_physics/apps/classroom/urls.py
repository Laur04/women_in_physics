from django.conf.urls import url

from . import views

app_name = 'classroom'

urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'^classroom/$', views.classroom, name='classroom'),
    url(r'^response/$', views.response, name='response'),
    url(r'^changestatus/(?P<post>\w+)/$', views.changestatus, name='changestatus'),
    url(r'^reset/student/$', views.reset_student, name='reset_student'),
]
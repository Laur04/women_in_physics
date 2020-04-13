from django.conf.urls import url

from . import views

app_name = 'classroom'

urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'^login/', views.login, name='login'),
    url(r'^classroom/(?P<classname>\w+)/(?P<person>\w+)/$', views.classroom, name='classroom'),
    url(r'^survey/(?P<classname>\w+)/$', views.survey, name='survey'),
    url(r'^changestatus/(?P<classname>\w+)/(?P<person>\w+)/(?P<post>\w+)/$', views.changestatus, name='changestatus'),
    url(r'^delete/(?P<classname>\w+)/$', views.delete, name='delete'),
]
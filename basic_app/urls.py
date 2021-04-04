from django.conf.urls import url
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    url(r'^todos/(?P<pk>\d+)/$', views.todos, name="todos"),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name="delete"),
    url(r'^done/(?P<pk>\d+)/$', views.done, name="done"),
    url(r'^undone/(?P<pk>\d+)/$', views.undone, name="undone"),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name="edit"),

    url(r'^add_todo/$', views.addTodo, name="addTodo"),

    url(r'^$', views.user_login, name="user_login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^user_logout/$', views.user_logout, name="user_logout"),



]

from django.conf.urls import url
from basic_app import views

urlpatterns=[
    url(r'^login/$', views.APIlogin),
    url(r'^register/$', views.RegisterAPIView),

    url(r'^todos/$', views.TodoListCreateAPIView.as_view()),
    url(r'^todo/(?P<pk>\d+)/$', views.TodoRetrieveUpdateDestroyAPIView.as_view()),
    url(r'^todo/mark/(?P<pk>\d+)/$', views.MarkTodoAPI.as_view()),



]

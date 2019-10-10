from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.post_list, name='post_list'),
    url('^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
]
from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.home, name='home'),
    url('^fifa_home/$', views.fifa_home, name='fifa_home'),
    url('^test/$', views.test, name='test'),
    url('^pagination/$', views.__pagination, name='_pagination'),
    url('^post_list/$', views.post_list, name='post_list'),
    url('^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url('^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url('^post/new/$', views.post_new, name='post_new'),
    url('^drafts/$', views.post_draft_list, name='post_draft_list'),
    url('^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url('^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url('^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url('^comment/(?P<pk>[0-9]+)/approve/$', views.comment_approve, name='comment_approve'),
    url('^comment/(?P<pk>[0-9]+)/remove/$', views.comment_remove, name='comment_remove'),
]
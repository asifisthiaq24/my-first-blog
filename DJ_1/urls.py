from django.contrib import admin
from django.conf.urls import url,include
from django.contrib.auth import views

urlpatterns = [
    url('^admin/$', admin.site.urls),
    url('^accounts/login/$', views.LoginView.as_view(), name='login'),
    url('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    url('', include('blog.urls')),
]
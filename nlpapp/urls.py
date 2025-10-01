from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'nlpapp'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('upload/',views.upload_file,name="upload"),
    path('login/',auth_views.LoginView.as_view(template_name='nlpapp/login.html'),name='login'),
    path('logout/',auth_views.LoginView.as_view(template_name='nlpapp/logout.html'),name='logout'),
    path('signup/',views.signup,name='signup'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),

    
]

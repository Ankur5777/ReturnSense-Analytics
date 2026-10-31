from django.urls import path
from . import views

urlpatterns = [
    # Change root '' to point to login_view instead of home
    path('', views.login_view, name='login'),
    
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.history, name='history'),
]
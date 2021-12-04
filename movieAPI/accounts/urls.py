from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),#Fix
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('viewProfile/', views.view_profile, name="view_profile"),
    path('editProfile/', views.edit_profile, name="edit_profile"),
]
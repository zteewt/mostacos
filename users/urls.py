from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Страница входа
    path('login/', views.login_view, name='login'),
    
    # Страница регистрации
    path('register/', views.register_view, name='register'),
    
    # Страница профиля (только для авторизованных)
    path('profile/', views.profile_view, name='profile'),
    
    # Выход из системы
    path('logout/', views.logout_view, name='logout'),
    
    # Сброс пароля (дополнительно)
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
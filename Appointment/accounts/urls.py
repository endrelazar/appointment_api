from django.urls import path
from . import views

urlpatterns = [
    path('delete-account/', views.delete_account, name='delete_account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
from django.urls import path
from django.contrib.auth.views import LogoutView
from user import views

app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile_update'),

    path('staff/add/', views.StaffCreateView.as_view(), name='staff_add'),
    path('staff/list/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/permission/', views.StaffPermissionView.as_view(), name='staff_permission'),
    path('staff/worksite/', views.StaffWorksiteView.as_view(), name='staff_worksite'),
]

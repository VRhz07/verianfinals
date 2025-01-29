from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from .views import (delete_progress_entry, edit_progress_entry, edit_workout_exercise, track_progress)

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='fitness/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('workout-programs/', views.WorkoutProgramListView.as_view(), name='workout_program_list'),
    path('workout-programs/create/', views.WorkoutProgramCreateView.as_view(), name='workout_program_create'),
    path('workout-programs/<int:pk>/update/', views.WorkoutProgramUpdateView.as_view(), name='workout_program_update'),
    path('workout-programs/<int:pk>/delete/', views.WorkoutProgramDeleteView.as_view(), name='workout_program_delete'),
    path('track-progress/', views.track_progress, name='track_progress'),
    path('user-workouts/', views.user_workouts, name='user_workouts'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('user-detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('workout-programs/<int:program_id>/add/', views.add_user_workout, name='add_user_workout'),
    path('user-workouts/', views.user_workouts, name='user_workouts'),
    path('complete-workout/<int:workout_id>/', views.complete_workout, name='complete_workout'),
    path('workout-program/<int:program_id>/add-exercise/', views.add_exercise_to_program, name='add_exercise_to_program'),
    path('workout-program/<int:pk>/', views.WorkoutProgramDetailView.as_view(), name='workout_program_detail'),
    path('workout-exercise/<int:exercise_id>/delete/', views.delete_workout_exercise, name='delete_workout_exercise'),
    path('edit_workout_exercise/<int:exercise_id>/', edit_workout_exercise, name='edit_workout_exercise'),
    path('remove-workout/<int:workout_id>/', views.remove_user_workout, name='remove_user_workout'),
    path('track_progress/', track_progress, name='track_progress'),
    path('track_progress/edit/<int:entry_id>/', edit_progress_entry, name='edit_progress_entry'),
    path('track_progress/delete/<int:entry_id>/', delete_progress_entry, name='delete_progress_entry'),

]
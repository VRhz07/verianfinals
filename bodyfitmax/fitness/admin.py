from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, WorkoutProgram, WorkoutDay, Exercise, WorkoutExercise, UserWorkout, UserProgress

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_area', 'difficulty', 'image')  # Include image in list display
    list_filter = ('target_area', 'difficulty')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'target_area', 'difficulty', 'image')  # Include image field
    inlines = [WorkoutExerciseInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'equipment_needed')
    list_filter = ('muscle_group', 'equipment_needed')
    search_fields = ('name', 'description')

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('workout_program', 'exercise', 'sets', 'reps')
    list_filter = ('workout_program', 'exercise')
    search_fields = ('workout_program__name', 'exercise__name')

@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_program', 'date', 'completed')
    list_filter = ('completed', 'date', 'workout_program')
    search_fields = ('user__username', 'workout_program__name')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight', 'body_fat_percentage')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
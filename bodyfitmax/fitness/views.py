from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import UserProfile, WorkoutProgram, UserWorkout, UserProgress, WorkoutExercise
from .forms import UserProfileForm, WorkoutProgramForm, UserProgressForm, WorkoutExerciseForm
from django.utils import timezone
from django.db.models import Q, Case, When, IntegerField, Value

def home(request):
    return render(request, 'fitness/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user instance
            user = form.save()
            
            # Check if a UserProfile already exists, then create if it doesn't
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Authenticate and log the user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('profile')  # Redirect to profile page
    else:
        form = UserCreationForm()
    
    return render(request, 'fitness/register.html', {'form': form})

@login_required
def profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'fitness/profile.html', {'form': form})

@login_required
def track_progress(request):
    progress = UserProgress.objects.filter(user=request.user).order_by('-date')
    
    if request.method == 'POST':
        form = UserProgressForm(request.POST)
        if form.is_valid():
            progress_entry = form.save(commit=False)
            progress_entry.user = request.user
            progress_entry.save()
            messages.success(request, 'Progress entry added successfully.')
            return redirect('track_progress')
    else:
        form = UserProgressForm(initial={'date': timezone.now().date()})
    
    return render(request, 'fitness/track_progress.html', {'progress': progress, 'form': form})

@login_required
def edit_progress_entry(request, entry_id):
    progress_entry = get_object_or_404(UserProgress, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = UserProgressForm(request.POST, instance=progress_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progress entry updated successfully.')
            return redirect('track_progress')
    else:
        form = UserProgressForm(instance=progress_entry)
    return render(request, 'fitness/edit_progress_entry.html', {'form': form})

@login_required
def delete_progress_entry(request, entry_id):
    progress_entry = get_object_or_404(UserProgress, id=entry_id, user=request.user)
    if request.method == 'POST':
        progress_entry.delete()
        messages.success(request, 'Progress entry deleted successfully.')
        return redirect('track_progress')
    return render(request, 'fitness/delete_progress_entry.html', {'entry': progress_entry})


@login_required
def user_workouts(request):
    workouts = UserWorkout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'fitness/user_workouts.html', {'workouts': workouts})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'fitness/manage_users.html', {'users': users})

@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = UserProfile.objects.get(user=user)
    return render(request, 'fitness/user_detail.html', {'user': user, 'profile': profile})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_exercise_to_program(request, program_id):
    program = get_object_or_404(WorkoutProgram, id=program_id)
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            workout_exercise = form.save(commit=False)
            workout_exercise.workout_program = program
            workout_exercise.order = WorkoutExercise.objects.filter(workout_program=program).count() + 1
            workout_exercise.save()
            messages.success(request, 'Exercise added successfully.')
            return redirect('add_exercise_to_program', program_id=program.id)
        else:
            print(form.errors)  # Debugging message
    else:
        form = WorkoutExerciseForm()
    
    exercises = WorkoutExercise.objects.filter(workout_program=program).order_by('order')
    return render(request, 'fitness/add_exercise_to_program.html', {
        'form': form,
        'program': program,
        'exercises': exercises,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_workout_exercise(request, exercise_id):
    workout_exercise = get_object_or_404(WorkoutExercise, id=exercise_id)
    program_id = workout_exercise.workout_program.id
    if request.method == 'POST':
        workout_exercise.delete()
        messages.success(request, 'Exercise removed successfully.')
    return redirect('add_exercise_to_program', program_id=program_id)

class WorkoutProgramListView(LoginRequiredMixin, ListView):
    model = WorkoutProgram
    template_name = 'fitness/workout_program_list.html'
    context_object_name = 'workout_programs'

    def get_queryset(self):
        queryset = WorkoutProgram.objects.all()
        query = self.request.GET.get('q')
        
        if query:
            conditions = (
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(target_area__icontains=query) |
                Q(difficulty__icontains=query)
            )
            
            queryset = queryset.annotate(
                is_match=Case(
                    When(conditions, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by('-is_match', '-id')  # Changed from 'name' to '-id'
        else:
            queryset = queryset.annotate(
                is_match=Value(0, output_field=IntegerField())
            ).order_by('-id')  # Changed from 'name' to '-id'
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class WorkoutProgramDetailView(DetailView):
    model = WorkoutProgram
    template_name = 'fitness/workout_program_detail.html'
    context_object_name = 'program'  # Changed from 'workout_program' to 'program' to match template

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class WorkoutProgramCreateView(AdminRequiredMixin, CreateView):
    model = WorkoutProgram
    form_class = WorkoutProgramForm
    template_name = 'fitness/workout_program_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Workout program created successfully. Now add exercises to your program.')
        return redirect('add_exercise_to_program', program_id=self.object.id)

    def get_success_url(self):
        return reverse('add_exercise_to_program', kwargs={'program_id': self.object.id})

class WorkoutProgramUpdateView(AdminRequiredMixin, UpdateView):
    model = WorkoutProgram
    form_class = WorkoutProgramForm
    template_name = 'fitness/workout_program_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Workout program updated successfully.')
        return response

    def get_success_url(self):
        return reverse('workout_program_detail', kwargs={'pk': self.object.id})


class WorkoutProgramUpdateView(AdminRequiredMixin, UpdateView):
    model = WorkoutProgram
    form_class = WorkoutProgramForm
    template_name = 'fitness/workout_program_form.html'
    success_url = reverse_lazy('workout_program_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Workout program updated successfully.')
        return response

class WorkoutProgramDeleteView(AdminRequiredMixin, DeleteView):
    model = WorkoutProgram
    template_name = 'fitness/workout_program_confirm_delete.html'
    success_url = reverse_lazy('workout_program_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Workout program deleted successfully.')
        return super().delete(request, *args, **kwargs)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def add_user_workout(request, program_id):
    program = get_object_or_404(WorkoutProgram, pk=program_id)
    UserWorkout.objects.create(user=request.user, workout_program=program, date=timezone.now())
    messages.success(request, f"Added {program.name} to your workouts.")
    return redirect('user_workouts')

class WorkoutProgramDetailView(DetailView):
    model = WorkoutProgram
    template_name = 'fitness/workout_program_detail.html'
    context_object_name = 'program'

@login_required
def complete_workout(request, workout_id):
    workout = get_object_or_404(UserWorkout, id=workout_id, user=request.user)
    workout.completed = True
    workout.save()
    messages.success(request, f"Workout '{workout.workout_program.name}' marked as completed!")
    return redirect('user_workouts')

login_required
@user_passes_test(lambda u: u.is_staff)
def edit_workout_exercise(request, exercise_id):
    workout_exercise = get_object_or_404(WorkoutExercise, id=exercise_id)
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST, instance=workout_exercise)
        if form.is_valid():
            workout_exercise = form.save(commit=False)
            rest_time_input = form.cleaned_data['rest_time']
            if isinstance(rest_time_input, str):
                if 'min' in rest_time_input:
                    minutes = int(rest_time_input.replace('min', '').strip())
                    workout_exercise.rest_time = timedelta(seconds=minutes * 60)
                else:
                    workout_exercise.rest_time = timedelta(seconds=int(rest_time_input))
            else:
                workout_exercise.rest_time = rest_time_input
            workout_exercise.save()
            messages.success(request, 'Exercise updated successfully.')
            return redirect('add_exercise_to_program', program_id=workout_exercise.workout_program.id)
    else:
        form = WorkoutExerciseForm(instance=workout_exercise)
    
    return render(request, 'fitness/edit_workout_exercise.html', {'form': form, 'workout_exercise': workout_exercise})

@login_required
def remove_user_workout(request, workout_id):
    workout = get_object_or_404(UserWorkout, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout removed successfully.')
    return redirect('user_workouts')

from datetime import timedelta
from django import forms
from .models import WorkoutProgram, WorkoutDay, WorkoutExercise, Exercise, UserProfile, UserProgress

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'height', 'weight', 'fitness_goal', 'activity_level', 'medical_conditions']
        labels = {'height': 'Height (cm)','weight': 'Weight (kg)',}
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
        }

class WorkoutProgramForm(forms.ModelForm):
    class Meta:
        model = WorkoutProgram
        fields = ['name', 'description', 'target_area', 'difficulty']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter program name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Enter program description'
            }),
            'target_area': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'E.g., Full Body, Upper Body, Lower Body'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long")
        return description

class WorkoutDayForm(forms.ModelForm):
    class Meta:
        model = WorkoutDay
        fields = ['name', 'order']

class WorkoutExerciseForm(forms.ModelForm):
    rest_time = forms.CharField(
        help_text="Enter rest time in seconds (e.g., '90') or minutes:seconds (e.g., '1:30')",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '90 or 1:30'
        })
    )
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'rest_time']
        widgets = {
            'exercise': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'sets': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'min': '1'
            }),
            'reps': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'min': '1'
            }),
           
        }

    def clean_rest_time(self):
        rest_time = self.cleaned_data.get('rest_time')
        try:
            if ':' in rest_time:
                minutes, seconds = map(int, rest_time.split(':'))
                return timedelta(minutes=minutes, seconds=seconds)
            else:
                return timedelta(seconds=int(rest_time))
        except ValueError:
            raise forms.ValidationError("Invalid rest time format. Use seconds (e.g., '90') or minutes:seconds (e.g., '1:30').")

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'equipment_needed', 'muscle_group']

class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['date', 'weight', 'body_fat_percentage', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.1'
            }),
            'body_fat_percentage': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3
            }),
        }

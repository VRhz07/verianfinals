# Generated by Django 5.1.2 on 2025-01-27 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_alter_workoutexercise_options_exercise_video_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workoutexercise',
            options={},
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='video_url',
        ),
    ]

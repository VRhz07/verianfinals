# Generated by Django 5.1.2 on 2025-01-23 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutprogram',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='workout_programs/'),
        ),
        migrations.AlterField(
            model_name='workoutexercise',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='workoutexercise',
            name='reps',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='workoutexercise',
            name='sets',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='workoutexercise',
            name='workout_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.workoutprogram'),
        ),
    ]

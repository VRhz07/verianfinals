# Generated by Django 5.1.2 on 2025-01-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_workoutprogram_image_alter_workoutexercise_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workoutexercise',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='exercise',
            name='video_url',
            field=models.URLField(blank=True, help_text='YouTube or other video demonstration link', null=True),
        ),
    ]

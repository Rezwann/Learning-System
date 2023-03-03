# Generated by Django 4.1.4 on 2022-12-29 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Quiz Name', max_length=100)),
                ('description', models.TextField(blank=True, default='Quiz Description', max_length=300, verbose_name='Quiz Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.channel')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creators', to=settings.AUTH_USER_MODEL)),
                ('intended_for', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('learning_subtask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.learningtask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectLearningOutcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=500)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.subject')),
            ],
        ),
        migrations.AddField(
            model_name='learningtask',
            name='learning_outcomes',
            field=models.ManyToManyField(to='Main.subjectlearningoutcome'),
        ),
        migrations.CreateModel(
            name='LearningSubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='Question', max_length=100)),
                ('hint', models.TextField(blank=True)),
                ('points', models.PositiveSmallIntegerField()),
                ('subtask_solution', models.TextField(default='Subtask solution', max_length=100)),
                ('learning_outcome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.subjectlearningoutcome')),
                ('learning_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.learningtask')),
            ],
        ),
    ]
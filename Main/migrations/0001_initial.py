# Generated by Django 4.1.4 on 2023-03-03 20:44

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Channel Name', max_length=100)),
                ('short_description', models.TextField(blank=True, default='Channel Description', max_length=300, verbose_name='Channel Description')),
            ],
        ),
        migrations.CreateModel(
            name='LearningBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Learning Board Name', max_length=300)),
                ('short_description', models.TextField(blank=True, default='Learning Board Description', max_length=300, verbose_name='Learning Board Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LearningBoardCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Learning Board Card Name', max_length=300)),
                ('short_description', models.TextField(blank=True, default='Learning Board Card Description', max_length=300, verbose_name='Card Description')),
                ('learning_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.learningboard')),
            ],
        ),
        migrations.CreateModel(
            name='LearningBoardCardList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Card List Name', max_length=50)),
                ('short_description', models.TextField(blank=True, default='Card List Description', max_length=300, verbose_name='Card List Description')),
            ],
        ),
        migrations.CreateModel(
            name='LearningTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Quiz Name', max_length=100)),
                ('description', models.TextField(blank=True, default='Quiz Description', max_length=300, verbose_name='Quiz Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('progress', models.FloatField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Science', 'Science'), ('English', 'English'), ('Mathematics', 'Mathematics'), ('French', 'French'), ('German', 'German'), ('Spanish', 'Spanish'), ('Mandarin', 'Mandarin'), ('Japanese', 'Japanese'), ('History', 'History'), ('Geography', 'Geography'), ('Economics', 'Economics'), ('Psychology', 'Psychology'), ('Sociology', 'Sociology'), ('Music', 'Music'), ('Drama', 'Drama'), ('Dance', 'Dance'), ('Computing', 'Computing'), ('Business', 'Business')], default='Computing', max_length=50)),
                ('details', models.CharField(default='', max_length=300)),
                ('year_group', models.CharField(choices=[('Year 7', 'Year 7'), ('Year 8', 'Year 8'), ('Year 9', 'Year 9'), ('Year 10', 'Year 10'), ('Year 11', 'Year 11')], default='Year_11', max_length=50)),
                ('subject_leader_name', models.CharField(default='', max_length=255)),
                ('subject_code', models.CharField(blank=True, max_length=8, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Modern Foreign Languages', 'Modern Foreign Languages'), ('Humanity', 'Humanity'), ('Arts', 'Arts'), ('Technical', 'Technical'), ('Core', 'Core')], max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Subject Categories (Departments)',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_information', models.TextField(blank=True, default='', max_length=300, verbose_name='User Information')),
                ('role', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student', max_length=20)),
                ('profile_image', models.ImageField(blank=True, default='profile_images/icon.png', null=True, upload_to='profile_images')),
                ('insight_verbal_memory_level', models.FloatField(default=0.0)),
                ('insight_non_verbal_memory_level', models.FloatField(default=0.0)),
                ('insight_visual_perception_level', models.FloatField(default=0.0)),
                ('insight_numeracy_level', models.FloatField(default=0.0)),
                ('insight_literacy_level', models.FloatField(default=0.0)),
                ('executive_function_level', models.FloatField(default=0.0)),
                ('visual_information_processing_speed_level', models.FloatField(default=0.0)),
                ('verbal_reasoning_level', models.FloatField(default=0.0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('subjects', models.ManyToManyField(to='Main.subject')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
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
            model_name='subject',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.subjectcategory'),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=300, verbose_name='Post Content')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.channel')),
            ],
        ),
        migrations.AddField(
            model_name='learningtask',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='learningtask',
            name='intended_for',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='LearningSubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='Question', max_length=100)),
                ('hint', models.TextField(blank=True)),
                ('points', models.PositiveSmallIntegerField()),
                ('subtask_solution', models.TextField(default='Subtask solution', max_length=100)),
                ('learning_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.learningtask')),
            ],
        ),
        migrations.CreateModel(
            name='LearningBoardWorkspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Learning Workspace', max_length=300)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LearningBoardCardTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Tag Name', max_length=50)),
                ('related_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.learningboardcard')),
            ],
        ),
        migrations.CreateModel(
            name='LearningBoardCardListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Learning Board Card List Item', max_length=50)),
                ('learning_board_card_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.learningboardcardlist')),
            ],
        ),
        migrations.AddField(
            model_name='learningboardcardlist',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='items', to='Main.learningboardcardlistitem'),
        ),
        migrations.AddField(
            model_name='learningboardcardlist',
            name='learning_board_card',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Main.learningboardcard'),
        ),
        migrations.AddField(
            model_name='learningboardcard',
            name='lists',
            field=models.ManyToManyField(blank=True, related_name='lists', to='Main.learningboardcardlist'),
        ),
        migrations.AddField(
            model_name='learningboardcard',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='cards', to='Main.learningboardcardtag'),
        ),
        migrations.AddField(
            model_name='learningboard',
            name='cards',
            field=models.ManyToManyField(blank=True, related_name='cards', to='Main.learningboardcard'),
        ),
        migrations.AddField(
            model_name='learningboard',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.learningboardworkspace'),
        ),
        migrations.CreateModel(
            name='CommunicationArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('related_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.subject')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='communication_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.communicationarea'),
        ),
    ]

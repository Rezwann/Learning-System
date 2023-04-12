import random
import string
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    user_information = models.TextField('User Information', max_length=300, default='', blank=True)
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    subjects = models.ManyToManyField('Subject')
    profile_image = models.ImageField(upload_to='profile_images', default="profile_images/icon.png", blank=True, null=True)

    verbal_memory_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    non_verbal_memory_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    visual_perception_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    visual_information_processing_speed_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    numeracy_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    literacy_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    executive_function_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    verbal_reasoning_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])    
    
    debate_contribution_target = models.FloatField(default=5)    
    VOCABULARY_CHOICES = (
        ('Very Low', 'Very Low'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Very High', 'Very High'),
    )
    
    vocabulary_sheet_group = models.CharField(max_length=20, choices=VOCABULARY_CHOICES, default='M') 

    ENG_TYPES = (
        ('Looking to participate', 'Looking to participate'),        
        ('Looking for discussion or group work', 'Looking for discussion or group work'),
        ('Looking to only listen in class', 'Looking to only listen in class'),
        ('Looking to uniquely contribute in class', 'Looking to uniquely contribute in class'),
        ('Looking to enagage in physical or hands-on activities', 'Looking to enagage in physical or hands-on activities'),
        ('Looking for occasional breaks or opportunities for quiet time', 'Looking for occasional breaks or opportunities for quiet time'),
    )
       
    desired_engagement_type = models.CharField(max_length=250, choices=ENG_TYPES, default='Looking to participate') 
       
    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            LearningBoardWorkspace.objects.create(user=self, name=f"{self.username}'s Workspace")
            EngagementInstance.objects.create(user=self, chosen_type=self.desired_engagement_type)

    @classmethod
    def validate_desired_engagement_type(cls, desired_engagement_type):
        if not any(desired_engagement_type == eng_type[0] for eng_type in cls.ENG_TYPES):
            raise ValidationError('Invalid engagement type choice.')

    def __str__(self):
        return self.username    

class EngagementInstance(models.Model):    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chosen_type = models.CharField(max_length=250, default='Looking to participate') 
    time_chosen = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return self.chosen_type

class SubjectCategory(models.Model):
    CATEGORY_CHOICES = (
        ('Modern Foreign Languages', 'Modern Foreign Languages'),
        ('Humanity', 'Humanity'),
        ('Arts', 'Arts'),
        ('Technical', 'Technical'),
        ('Core', 'Core'),
    )    
    
    name = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    
    class Meta:
        verbose_name_plural = "Subject Categories (Departments)"
    
    def __str__(self):
        return self.name
        
class Subject(models.Model):
    SUBJECT_CHOICES = (
        ("Science","Science"),
        ("English","English"),
        ("Mathematics","Mathematics"),
        ("French","French"),
        ("German","German"),
        ("Spanish","Spanish"),
        ("Mandarin","Mandarin"),
        ("Japanese","Japanese"),
        ("History","History"),
        ("Geography","Geography"),
        ("Economics","Economics"),
        ("Psychology","Psychology"),
        ("Sociology","Sociology"),
        ("Music","Music"),
        ("Drama","Drama"),
        ("Dance","Dance"),
        ("Computing","Computing"),
        ("Business","Business"),
    )
    
    YEAR_CHOICES = (
        ('Year 7', 'Year 7'),
        ('Year 8', 'Year 8'),
        ('Year 9', 'Year 9'),
        ('Year 10', 'Year 10'),
        ('Year 11', 'Year 11'),

    )
            
    name = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='Computing')
    details = models.CharField(max_length=300, default='')
    
    category = models.ForeignKey(SubjectCategory, on_delete=models.CASCADE)
    year_group = models.CharField(max_length=50, choices=YEAR_CHOICES, default='Year_11')   
    subject_leader_name = models.CharField(max_length=255, default = '')
    subject_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leader')
    subject_code = models.CharField(max_length=8, unique=True, blank=True, null = True)
    users = models.ManyToManyField(CustomUser)
        
    def save(self, *args, **kwargs):
        if not self.subject_code:
            name_code = self.name[0]
            random_code = ''.join(random.choices(string.digits, k=4))
            self.subject_code = f'{name_code}{random_code}'        
        if not self.subject_leader_name:
            self.subject_leader_name = self.subject_leader.username.capitalize()

        if not self.subject_leader_name[0].isupper():
            self.subject_leader_name = self.subject_leader_name.capitalize()
            
        super().save(*args, **kwargs)
        CommunicationArea.objects.create(related_subject=self)
        
    def __str__(self):
        return f"{self.name}, {self.subject_code}, {self.year_group}"        

class CommunicationArea(models.Model):
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.related_subject.name} - {self.related_subject.subject_code} Area"
        super().save(*args, **kwargs)
        if not self.channel_set.filter(name='Main Channel').exists():        
            Channel.objects.create(communication_area=self, name=f"{self.related_subject.name} ({self.related_subject.subject_code}) - Main Channel", short_description = 'Main Channel Description')

    def __str__(self):
        return f"{self.related_subject}, {self.name}"

class Channel(models.Model):
    communication_area = models.ForeignKey(CommunicationArea, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Channel Name')
    short_description = models.TextField('Channel Description', max_length=300, default='Channel Description', blank=True)

    def __str__(self):
        return f"{self.communication_area}, {self.name}"

class Post(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField('Post Content', max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class LearningBoardWorkspace(models.Model):
    name = models.CharField(max_length=300, default='Learning Workspace')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
board_role = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
)    

class LearningBoard(models.Model):                
    name = models.CharField(max_length=300,  default='Learning Board Name')
    short_description = models.TextField('Learning Board Description', max_length=300, default='Learning Board Description', blank=True)
    cards = models.ManyToManyField('LearningBoardCard', related_name='cards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    workspace = models.ForeignKey('LearningBoardWorkspace', on_delete=models.CASCADE)
    board_type = models.CharField(max_length=40, choices=board_role, default='Student')

    def __str__(self):
        return self.name

class LearningBoardCard(models.Model):
    learning_board = models.ForeignKey(LearningBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default='Learning Board Card Name')
    short_description = models.TextField('Card Description', max_length=300, default='Learning Board Card Description', blank=True)
    lists = models.ManyToManyField('LearningBoardCardList', related_name='lists', blank=True)
    tags = models.ManyToManyField('LearningBoardCardTag', related_name='cards', blank=True)
    def __str__(self):
        return self.name
    
class LearningBoardCardTag(models.Model):
    related_card = models.ForeignKey(LearningBoardCard, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Tag Name')
    
    def __str__(self):
        return self.name

class LearningBoardCardList(models.Model):
    learning_board_card = models.ForeignKey(LearningBoardCard, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=50, default = 'Card List Name')
    short_description = models.TextField('Card List Description', max_length=300, default='Card List Description', blank=True)
    items = models.ManyToManyField('LearningBoardCardListItem', related_name='items', blank=True)
    def __str__(self):
        return self.name

class LearningBoardCardListItem(models.Model):
    learning_board_card_list = models.ForeignKey(LearningBoardCardList, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Learning Board Card List Item')
    
    def __str__(self):
        return self.name
    

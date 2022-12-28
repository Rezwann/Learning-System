import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_information = models.TextField('User Information', max_length=300, default='', blank=True)
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    subjects = models.ManyToManyField('Subject')
    
    def __str__(self):
        return self.username    

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
        super().save(*args, **kwargs)
        
        # Create CommunicationArea for a Subject instance
        CommunicationArea.objects.create(related_subject=self)
        
    def __str__(self):
        return f"{self.name}, {self.subject_code}, {self.year_group}"        

# Subject Communication Area
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

# Learning Workplace/Learning Boards

class LearningBoard(models.Model):                
    name = models.CharField(max_length=300,  default='Learning Board Name')
    short_description = models.TextField('Learning Board Description', max_length=300, default='Learning Board Description', blank=True)
    cards = models.ManyToManyField('LearningBoardCard', related_name='cards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
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
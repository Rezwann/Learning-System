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
        
    def save(self, *args, **kwargs):
        if not self.subject_code:
            name_code = self.name[0]
            random_code = ''.join(random.choices(string.digits, k=4))
            self.subject_code = f'{name_code}{random_code}'        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class LearningBoard(models.Model):                
    name = models.CharField(max_length=50)
    short_description = models.TextField('Learning Board Description', max_length=300, default='', blank=True)
    cards = models.ManyToManyField('LearningBoardCard', related_name='cards', blank=True)    

    def __str__(self):
        return self.name

class LearningBoardCard(models.Model):
    learning_board = models.ForeignKey(LearningBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_description = models.TextField('Card Description', max_length=300, default='', blank=True)
    lists = models.ManyToManyField('LearningBoardCardList', related_name='lists', blank=True)
    tags = models.ManyToManyField('LearningBoardCardTag', related_name='cards', blank=True)
    def __str__(self):
        return self.name

class LearningBoardCardList(models.Model):
    learning_board_card = models.ForeignKey(LearningBoardCard, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_description = models.TextField('Card List Description', max_length=300, default='', blank=True)
    items = models.ManyToManyField('LearningBoardCardListItem', related_name='items', blank=True)
    def __str__(self):
        return self.name

class LearningBoardCardListItem(models.Model):
    learning_board_card_list = models.ForeignKey(LearningBoardCardList, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class LearningBoardCardTag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
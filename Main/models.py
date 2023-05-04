import random
import string
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F


class CustomUser(AbstractUser):
    user_information = models.TextField('User Information', max_length=300, default='', blank=True)
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    subjects = models.ManyToManyField('Subject')
    profile_image = models.ImageField(upload_to='profile_images', default="profile_images/icon.png", blank=True, null=True)    
    hasEHCP = models.BooleanField(default=True)    
    verbal_memory_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    non_verbal_memory_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    visual_perception_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    visual_information_processing_speed_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    numeracy_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    literacy_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    executive_function_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
    verbal_reasoning_level = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])    
    averageCD = models.FloatField(default=50.0, validators=[MinValueValidator(1.0), MaxValueValidator(100.0)])
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
        cd_values = [self.verbal_memory_level, self.non_verbal_memory_level, 
        self.visual_perception_level, self.visual_information_processing_speed_level, 
        self.numeracy_level, self.literacy_level, 
        self.executive_function_level, self.verbal_reasoning_level]
        average_cd = sum(cd_values) / len(cd_values)
        self.averageCD = round(average_cd)        
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            EHCP_Interest.objects.create(user=self)
            EHCP_Aspiration.objects.create(user=self)
            EHCP_View.objects.create(user=self)
            self.create_missing_categories()
            workspace = LearningBoardWorkspace.objects.create(user=self, name=f"{self.username}'s Workspace")
            LB = LearningBoard.objects.create(name=f"{self.username}'s First Learning Board", short_description="Here is an example description for each learning board :)", workspace=workspace)
            LBC = LearningBoardCard.objects.create(learning_board = LB, name=f"{self.username}'s First Learning Board Card", short_description="Here is an example description for a card :)")
            LBCL = LearningBoardCardList.objects.create(learning_board_card = LBC, name=f"{self.username}'s First Learning List", short_description="Here is an example descripiton for a list :)")
            LearningBoardCardListItem.objects.create(learning_board_card_list = LBCL, name=f"{self.username}'s First default List Item")
            LearningBoardCardListItem.objects.create(learning_board_card_list = LBCL, name=f"{self.username}'s Second default List Item")
            LearningBoardCardListItem.objects.create(learning_board_card_list = LBCL, name=f"{self.username}'s Third default List Item")
            EngagementInstance.objects.create(user=self, chosen_type=self.desired_engagement_type)
                        
    def __str__(self):
        return self.name

    @classmethod
    def validate_desired_engagement_type(cls, desired_engagement_type):
        if not any(desired_engagement_type == eng_type[0] for eng_type in cls.ENG_TYPES):
            raise ValidationError('Invalid engagement type choice.')

    @classmethod
    def create_missing_categories(cls):
            CATEGORY_CHOICES = (
                ('Modern Foreign Languages', 'Modern Foreign Languages'),
                ('Humanity', 'Humanity'),
                ('Arts', 'Arts'),
                ('Technical', 'Technical'),
                ('Core', 'Core'),
            )
            existing_categories = set(category.name for category in SubjectCategory.objects.all())
            for category_choice in CATEGORY_CHOICES:
                if category_choice[0] not in existing_categories:
                    SubjectCategory.objects.create(name=category_choice[0])

    def __str__(self):
        return self.username    

class EngagementInstance(models.Model):    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chosen_type = models.CharField(max_length=250, default='Looking to participate') 
    time_chosen = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return self.chosen_type

class EHCP_View(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_views = models.TextField('EHCP Views', max_length=300, default="Student's Views from EHCP - not setup yet", blank=True)
    teacher_comments = models.ManyToManyField('EHCP_TeacherComment', related_name='ehcp_views', blank=True)
 
    class Meta:
        verbose_name_plural = "EHCP Views"
    
    def __str__(self):
        return f"{self.user}, {self.student_views}" 

class EHCP_Interest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_interests = models.TextField('EHCP Interests', max_length=300, default="Student's Interests from EHCP - not setup yet", blank=True)
    teacher_comments = models.ManyToManyField('EHCP_TeacherComment', related_name='ehcp_interests', blank=True)

    class Meta:
        verbose_name_plural = "EHCP Interests"
 
    def __str__(self):
        return f"{self.user}, {self.student_interests}"
 
class EHCP_Aspiration(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_aspirations = models.TextField('EHCP Aspirations', max_length=300, default="Student's Aspirations from EHCP - not setup yet", blank=True)
    teacher_comments = models.ManyToManyField('EHCP_TeacherComment', related_name='ehcp_aspirations', blank=True)

    class Meta:
        verbose_name_plural = "EHCP Aspirations"
        
    def __str__(self):
        return f"{self.user}, {self.student_aspirations}"        

class EHCP_TeacherComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField('Teacher Comment', max_length=300, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "EHCP Teacher Comments"
        
    def __str__(self):
        return f"{self.user}, {self.comment}"        
        
# Overview - Subjects        
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
    
    @classmethod
    def create(cls, name):
        category = cls(name=name)
        category.save()
        return category
    
    def __str__(self):
        return self.name
        
class Subject(models.Model):
    SUBJECT_CHOICES = (
        ("Science","Science"), ("English","English"),
        ("Mathematics","Mathematics"), ("French","French"),
        ("German","German"), ("Spanish","Spanish"),
        ("Mandarin","Mandarin"), ("Japanese","Japanese"),
        ("History","History"), ("Geography","Geography"),
        ("Economics","Economics"), ("Psychology","Psychology"),
        ("Sociology","Sociology"), ("Music","Music"),
        ("Drama","Drama"), ("Dance","Dance"),
        ("Computing","Computing"), ("Business","Business"),
    )
    
    YEAR_CHOICES = (
        ('Year 7', 'Year 7'), ('Year 8', 'Year 8'),
        ('Year 9', 'Year 9'), ('Year 10', 'Year 10'),
        ('Year 11', 'Year 11'),
    )
            
    name = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='Computing')
    details = models.CharField(max_length=300, default='', blank=True, null = True)    
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
            
        if not self.details:                      
            self.details = "Details"

        super().save(*args, **kwargs)

        try:
            CommunicationArea.objects.get(related_subject=self)
        except ObjectDoesNotExist:
            CommunicationArea.objects.create(related_subject=self)
        try:
            DebatingArea.objects.get(related_subject=self)
        except ObjectDoesNotExist:
            DebatingArea.objects.create(related_subject=self)         
    def __str__(self):
        return f"{self.name}, {self.subject_code}, {self.year_group}"        

# Subject-speciifc Debating Activity

class DebatingArea(models.Model):
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='', blank=True)
    debate_question = models.CharField(max_length=255, default='', blank=True)
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.related_subject.name} - {self.related_subject.subject_code} Debating Area"
        if not self.debate_question:
            self.debate_question = f"Is the subject {self.related_subject.name} reaching enough people in the world? 🌍"
        super().save(*args, **kwargs)                
        DebateSide.objects.create(debating_area=self, side_name=f'{self.related_subject.subject_code} Side - Yes')
        DebateSide.objects.create(debating_area=self, side_name=f'{self.related_subject.subject_code} Side - Nope')
        DebateSide.objects.create(debating_area=self, side_name=f'{self.related_subject.subject_code} Side - Unsure')        
    def __str__(self):
        return f"{self.related_subject}, {self.name}, Debating Area"

class DebateSide(models.Model):
    debating_area = models.ForeignKey(DebatingArea, on_delete=models.CASCADE, 
    related_name='sides')
    side_name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.side_name}, {self.debating_area}"

class DebatingContribution(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    debating_area = models.ForeignKey(DebatingArea, on_delete=models.CASCADE)
    amount_contributed = models.IntegerField(default=0)

class Opinion(models.Model):
    debate_side = models.ForeignKey(DebateSide, on_delete=models.CASCADE, related_name='opinions')
    text = models.CharField(max_length=255, default='No text was given.', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only increment on creation
            debating_contribution, created = DebatingContribution.objects.get_or_create(
                user=self.author,
                debating_area=self.debate_side.debating_area
            )
            debating_contribution.amount_contributed = F('amount_contributed') + 1
            debating_contribution.save()
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        debating_contribution = DebatingContribution.objects.get(
            user=self.author,
            debating_area=self.debate_side.debating_area
        )
        debating_contribution.amount_contributed = F('amount_contributed') - 1
        debating_contribution.save()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return f"{self.debate_side}, opinion - {self.text}"


# Overview - Communication Area

class CommunicationArea(models.Model):
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='', blank=True)    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.related_subject.name} - {self.related_subject.subject_code} Area"
        super().save(*args, **kwargs)
        if not self.channel_set.filter(name='Main Channel').exists():        
            Channel.objects.create(communication_area=self, name=f"{self.related_subject.name} ({self.related_subject.subject_code}) - Main Channel", short_description = 'Main Channel Description')
            Channel.objects.create(communication_area=self, name=f"{self.related_subject.name} ({self.related_subject.subject_code}) - 🐧", short_description = '🐧 Channel Description')
            Channel.objects.create(communication_area=self, name=f"{self.related_subject.name} ({self.related_subject.subject_code}) - 🦒", short_description = '🦒 Channel Description')
            Channel.objects.create(communication_area=self, name=f"{self.related_subject.name} ({self.related_subject.subject_code}) - 🐅", short_description = '🐅 Channel Description')
            Channel.objects.create(communication_area=self, name=f"{self.related_subject.name} ({self.related_subject.subject_code}) - 🦈", short_description = '🦈 Channel Description')
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

# Learning Workspace

class LearningBoardWorkspace(models.Model):
    name = models.CharField(max_length=300, default='Learning Workspace')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.name    
board_role = (('Student', 'Student'), ('Teacher', 'Teacher'),)    

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
    file_attachment = models.FileField(upload_to='card_attachments/', null=True, blank=True)

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
    
    
    

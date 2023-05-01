from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem
from .models import CommunicationArea, Channel, Post
from .models import  LearningBoardWorkspace, EngagementInstance, DebatingArea
from .models import EHCP_View, EHCP_Interest, EHCP_Aspiration, EHCP_TeacherComment
from .models import DebatingArea, DebateSide, DebatingContribution, Opinion

class CustomUserAdmin(UserAdmin):
    model = CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {
            'fields': ('user_information', 'role', 'subjects', 'profile_image')
        }),
        ('All', {
            'fields': (
                'averageCD','hasEHCP','verbal_memory_level', 
                'non_verbal_memory_level', 'visual_perception_level', 
                'numeracy_level', 'literacy_level', 'executive_function_level', 'visual_information_processing_speed_level', 
                'verbal_reasoning_level', 'debate_contribution_target', 'vocabulary_sheet_group', 'desired_engagement_type'                
            )
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
class CommunicationAreaAdmin(admin.ModelAdmin):
    list_display = ('related_subject',)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('communication_area', 'name', 'short_description')
class PostAdmin(admin.ModelAdmin):
    list_display = ('channel', 'author', 'content', 'created_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(SubjectCategory)
admin.site.register(LearningBoardWorkspace)
admin.site.register(LearningBoard)
admin.site.register(LearningBoardCard)
admin.site.register(LearningBoardCardList)
admin.site.register(LearningBoardCardListItem)
admin.site.register(CommunicationArea, CommunicationAreaAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(EngagementInstance)
admin.site.register(EHCP_View)
admin.site.register(EHCP_Interest)
admin.site.register(EHCP_Aspiration)
admin.site.register(EHCP_TeacherComment)
admin.site.register(DebatingArea)
admin.site.register(DebateSide)
admin.site.register(DebatingContribution)
admin.site.register(Opinion)
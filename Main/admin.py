from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag
from .models import CommunicationArea, Channel, Post

class CustomUserAdmin(UserAdmin):
    model = CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_information',)}),
        (None, {'fields': ('role',)}),
        (None, {'fields': ('subjects',)}),
        (None, {'fields': ('profile_image',)}),
        )

class CommunicationAreaAdmin(admin.ModelAdmin):
    list_display = ('related_subject',)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('communication_area', 'name', 'short_description')

class PostAdmin(admin.ModelAdmin):
    list_display = ('channel', 'author', 'content', 'created_at')
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(SubjectCategory)
admin.site.register(LearningBoard)
admin.site.register(LearningBoardCard)
admin.site.register(LearningBoardCardTag)
admin.site.register(LearningBoardCardList)
admin.site.register(LearningBoardCardListItem)
admin.site.register(CommunicationArea, CommunicationAreaAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Post, PostAdmin)

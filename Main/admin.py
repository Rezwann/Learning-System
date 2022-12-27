from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag

class CustomUserAdmin(UserAdmin):
    model = CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_information',)}),
        (None, {'fields': ('role',)}),
        (None, {'fields': ('subjects',)}),
        )
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(SubjectCategory)
admin.site.register(LearningBoard)
admin.site.register(LearningBoardCard)
admin.site.register(LearningBoardCardTag)
admin.site.register(LearningBoardCardList)
admin.site.register(LearningBoardCardListItem)
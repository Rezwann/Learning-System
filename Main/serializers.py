from rest_framework import serializers
from .models import CustomUser, Subject, SubjectCategory, LearningBoardWorkspace, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag
from .models import CommunicationArea, Channel, Post
from .models import EngagementInstance

class CustomUserSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    ENG_TYPES = CustomUser.ENG_TYPES

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'user_information', 'role', 'subjects', 
                  'profile_image', 'profile_image_url','verbal_memory_level'
                  ,'non_verbal_memory_level', 'visual_perception_level',
                  'visual_information_processing_speed_level',
                  'numeracy_level', 'literacy_level', 'executive_function_level',
                  'verbal_reasoning_level', 'debate_contribution_target',
                  'vocabulary_sheet_group', 'desired_engagement_type',                  
                  'ENG_TYPES')
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None

class EngagementInstanceSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = EngagementInstance
        fields = ('id','user', 'username', 'chosen_type', 'time_chosen')

class SubjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    subject_leader_email = serializers.CharField(source='subject_leader.email')

    class Meta:
        model = Subject
        fields = ('id', 'name', 'details', 'category', 'category_name', 'year_group', 
                  'subject_leader_name', 'subject_leader', 'subject_leader_email',
                  'subject_code')

class SubjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCategory
        fields = ('id', 'name')
        
class CommunicationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationArea
        fields = ['id', 'related_subject_id', 'name']                

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'communication_area_id', 'name', 'short_description']

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_role = serializers.CharField(source='author.role', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'channel_id', 'author', 'author_username', 'author_role', 'content', 'created_at']

class LearningBoardWorkspaceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = LearningBoardWorkspace
        fields = ('id', 'name', 'user', 'username')       

class LearningBoardSerializer(serializers.ModelSerializer):                
    class Meta:
        model = LearningBoard
        fields = ('id', 'name', 'short_description', 'cards', 'created_at', 'board_type')

class LearningBoardCardTagSerializer(serializers.ModelSerializer):                
    class Meta:
        model = LearningBoardCardTag
        fields = ('id','name', 'related_card_id')
        
class LearningBoardCardSerializer(serializers.ModelSerializer):
    learning_board_id = serializers.SerializerMethodField()

    class Meta:
        model = LearningBoardCard
        fields = ('id', 'learning_board_id','name', 'short_description', 
                  'lists','tags')
    
    def get_learning_board_id(self, obj):
        return obj.learning_board.id
    
class LearningBoardCardListSerializer(serializers.ModelSerializer):                
    learning_board_card_id = serializers.SerializerMethodField()

    class Meta:
        model = LearningBoardCardList
        fields = ('id', 'learning_board_card_id','name', 'short_description', 
                  'items')
        
    def get_learning_board_card_id(self, obj):
        return obj.learning_board_card.id


class LearningBoardCardListItemSerializer(serializers.ModelSerializer):                
    learning_board_card_list_id = serializers.SerializerMethodField()
    class Meta:
        model = LearningBoardCardListItem
        fields = ('id', 'learning_board_card_list_id','name')
    def get_learning_board_card_list_id(self, obj):
        return obj.learning_board_card_list.id
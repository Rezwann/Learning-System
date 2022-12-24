from rest_framework import serializers
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag


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

class LearningBoardSerializer(serializers.ModelSerializer):                
    class Meta:
        model = LearningBoard
        fields = ('id', 'name', 'short_description', 'cards')

class LearningBoardCardSerializer(serializers.ModelSerializer):                
    class Meta:
        model = LearningBoardCard
        fields = ('id', 'learning_board','name', 'short_description', 
                  'lists','tags')

class LearningBoardCardListSerializer(serializers.ModelSerializer):                
    class Meta:
        model = LearningBoardCardList
        fields = ('id', 'learning_board_card','name', 'short_description', 
                  'items')

class LearningBoardCardListItemSerializer(serializers.ModelSerializer):                
    class Meta:
        model = LearningBoardCardListItem
        fields = ('id', 'learning_board_card_list','name')
    
class LearningBoardCardListItemSerializer(serializers.ModelSerializer):                
    class Meta:
        model = LearningBoardCardTag
        fields = ('id','name')
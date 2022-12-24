from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Subject, SubjectCategory, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag

from .serializers import SubjectSerializer, SubjectCategorySerializer, LearningBoardSerializer, LearningBoardCardSerializer
from .serializers import LearningBoardCardListSerializer, LearningBoardCardListItemSerializer
from .serializers import LearningBoardCardListItemSerializer

@api_view(['GET'])
def get_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_subject_categories(request):
    subject_categories = SubjectCategory.objects.all()
    serializer = SubjectCategorySerializer(subject_categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_learning_boards(request):
    learning_boards = LearningBoard.objects.all()
    serializer = LearningBoardSerializer(learning_boards, many=True)
    return Response(serializer.data)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

from .models import Subject, SubjectCategory, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag

from .serializers import SubjectSerializer, SubjectCategorySerializer, LearningBoardSerializer, LearningBoardCardSerializer
from .serializers import LearningBoardCardListSerializer, LearningBoardCardListItemSerializer
from .serializers import LearningBoardCardListItemSerializer, LearningBoardCardTagSerializer

@api_view(['GET'])
def get_subjects(request):
    user = request.user
    subjects = user.subjects.all()
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

@api_view(['GET'])
def get_learning_boards_cards(request):
    learning_boards_cards = LearningBoardCard.objects.all()
    serializer = LearningBoardCardSerializer(learning_boards_cards, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_learning_boards_cards_tags(request):
    learning_boards_cards_tags = LearningBoardCardTag.objects.all()
    serializer = LearningBoardCardTagSerializer(learning_boards_cards_tags, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_learning_boards_cards_lists(request):
    learning_boards_cards_lists = LearningBoardCardList.objects.all()
    serializer = LearningBoardCardListSerializer(learning_boards_cards_lists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_learning_boards_cards_lists_items(request):
    learning_boards_cards_lists_items = LearningBoardCardListItem.objects.all()
    serializer = LearningBoardCardListItemSerializer(learning_boards_cards_lists_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_learning_board(request):
    print(request.data)
    
    new_board = LearningBoard.objects.create(
        name = request.data.get('name'),
        short_description = request.data.get('short_description')        
    )
    
    new_board.save()
    
    print(new_board)
    
    return Response({'added:added'})

@api_view(['POST'])
def delete_learning_board(request):
    learningboard_id = request.data.get('num')
    learningboard = LearningBoard.objects.get(id=learningboard_id)
    learningboard.delete()
             
    return Response({'deleted:deleted'})

@api_view(['POST'])
def delete_learning_board_card(request):
    learningboardcard_id = request.data.get('num')
    learningboardcard = LearningBoardCard.objects.get(id=learningboardcard_id)
    learningboardcard.delete()
             
    return Response({'deleted:deleted'})

@api_view(['GET'])
def get_current_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        return JsonResponse({'username': username})
    else:
        return JsonResponse({'error': 'User is not authenticated'})
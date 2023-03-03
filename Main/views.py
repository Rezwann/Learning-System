from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag
from .models import CommunicationArea, Channel, Post

from .serializers import CustomUserSerializer, SubjectSerializer, SubjectCategorySerializer, LearningBoardSerializer, LearningBoardCardSerializer
from .serializers import LearningBoardCardListSerializer, LearningBoardCardListItemSerializer
from .serializers import LearningBoardCardListItemSerializer, LearningBoardCardTagSerializer
from .serializers import CommunicationAreaSerializer, ChannelSerializer, PostSerializer

@api_view(['GET'])
def get_custom_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_subjects(request):
    user = request.user
    # Get all subjects where the user is in the users field
    subjects = Subject.objects.filter(Q(users=user))
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_subject_categories(request):
    subject_categories = SubjectCategory.objects.all()
    serializer = SubjectCategorySerializer(subject_categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_communication_areas(request):
    communication_areas = CommunicationArea.objects.all()
    serializer = CommunicationAreaSerializer(communication_areas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_channels(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def get_posts(request):
    cid = request.data.get('num')
    posts = Post.objects.filter(channel_id=cid)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_channel_post(request):
    channel_passed = Channel.objects.get(id=request.data.get('num'))
    user = request.user    

    if (request.data.get('content') != ''):
        new_post = Post.objects.create(
            channel = channel_passed,
            author = user, content = request.data.get('content')        
        )    
        new_post.save()    
    
    return Response({'added:added'})


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

@api_view(['POST'])
def add_learning_board_card(request):
    learningboard_id = request.data.get('num')
    new_card_name = request.data.get('name')
    new_card_desc = request.data.get('description')
    learningboard = LearningBoard.objects.get(id=learningboard_id)
    
    new_card = LearningBoardCard.objects.create(
        name=new_card_name,
        short_description=new_card_desc,
        learning_board=learningboard
    )
    new_card.save()
    
    serializer = LearningBoardCardSerializer(new_card)
    return Response(serializer.data)

@api_view(['GET'])
def get_current_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        role = request.user.role        
        return JsonResponse({'username': username, 'role':role})
    else:
        return JsonResponse({'error': 'User is not authenticated'})
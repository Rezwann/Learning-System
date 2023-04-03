from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardWorkspace, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem, LearningBoardCardTag
from .models import CommunicationArea, Channel, Post
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, SubjectSerializer, SubjectCategorySerializer, LearningBoardSerializer, LearningBoardCardSerializer
from .serializers import LearningBoardCardListSerializer, LearningBoardCardListItemSerializer
from .serializers import LearningBoardCardListItemSerializer, LearningBoardCardTagSerializer
from .serializers import CommunicationAreaSerializer, ChannelSerializer, PostSerializer, LearningBoardWorkspaceSerializer
import math
import sklearn
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Define the decision tree model
model = DecisionTreeClassifier(random_state=42, max_depth=3)

# Define the vocabulary groups and their corresponding labels
vocabulary_groups = {
    'Very Low': 0,
    'Low': 1,
    'Medium': 2,
    'High': 3,
    'Very High': 4
}

# Define the decision tree rules based on the input features
rules = [
    {'feature': 'VM', 'threshold': 30},
    {'feature': 'NVM', 'threshold': 30},
    {'feature': 'L', 'threshold': 30},
    {'feature': 'EF', 'threshold': 30},
]

# Convert the input features to a 2D array
X = np.array([[VM, NVM, L, EF]])

# Predict the vocabulary group using the decision tree model
predicted_group = model.fit(X, [0]).predict(X)[0]

# Assign the predicted vocabulary group to the corresponding label
vocab_group = list(vocabulary_groups.keys())[list(vocabulary_groups.values()).index(predicted_group)]



@api_view(['GET'])
def get_custom_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def get_user_neurobackground(request):
    try:
        username = request.data.get('studentname')
        user = CustomUser.objects.get(username=username)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist.'})
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['POST'])
def update_student_neuro_background(request):
    VM = float(request.data.get('VM'))
    NVM = float(request.data.get('NVM'))
    VP = float(request.data.get('VP'))
    VIPS = float(request.data.get('VIPS'))
    N = float(request.data.get('N'))
    L = float(request.data.get('L'))
    EF =  float(request.data.get('EF'))
    VR = float(request.data.get('VR'))

    # debate
    base_target = 5.0     
    addition_for_base_target = ((VM*0.2)+(NVM*0.05)+(VP*0.1)+(VIPS*0.1)+(N*0.05)+(L*0.15)
    +(EF*0.15) + (VR*0.3))    
    final_debate_target = base_target + (base_target*(2*(addition_for_base_target/100.0)))
    final_debate_target_rounded = math.ceil(final_debate_target)
    print(final_debate_target_rounded)
    
    # vocabulary sheet group
    
    VM, NVM, L, EF, 
                
        
    studentname = request.data.get('studentname')
    user = CustomUser.objects.get(username=studentname)    
    user.verbal_memory_level = VM
    user.non_verbal_memory_level = NVM
    user.visual_perception_level = VP
    user.visual_information_processing_speed_level = VIPS
    user.numeracy_level = N
    user.literacy_level = L
    user.executive_function_level = EF
    user.verbal_reasoning_level = VR    
    user.debate_contribution_target = final_debate_target_rounded
    user.save()
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_subjects(request):
    user = request.user
    subjects = Subject.objects.filter(Q(users=user) | Q(subject_leader=user))
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
def get_learning_workspace(request):
    user = request.user
    learning_workspace = LearningBoardWorkspace.objects.filter(user=user)
    serializer = LearningBoardWorkspaceSerializer(learning_workspace, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_learning_boards(request):
    user_workspace = request.user.learningboardworkspace
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    serializer = LearningBoardSerializer(learning_boards, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_learning_boards_cards(request):
    user_workspace = LearningBoardWorkspace.objects.get(user=request.user)
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    learning_boards_cards = LearningBoardCard.objects.filter(learning_board__in=learning_boards)
    serializer = LearningBoardCardSerializer(learning_boards_cards, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_learning_boards_cards_tags(request):
    user_workspace = request.user.learningboardworkspace
    learning_boards_cards_tags = LearningBoardCardTag.objects.filter(related_card__learning_board__workspace=user_workspace)
    serializer = LearningBoardCardTagSerializer(learning_boards_cards_tags, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_learning_boards_cards_lists(request):
    user_workspace = LearningBoardWorkspace.objects.get(user=request.user)
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    learning_boards_cards_lists = LearningBoardCardList.objects.filter(learning_board_card__learning_board__in=learning_boards)
    serializer = LearningBoardCardListSerializer(learning_boards_cards_lists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_learning_boards_cards_lists_items(request):
    user_workspace = LearningBoardWorkspace.objects.get(user=request.user)
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    learning_boards_cards_lists_items = LearningBoardCardListItem.objects.filter(learning_board_card_list__learning_board_card__learning_board__in=learning_boards)
    serializer = LearningBoardCardListItemSerializer(learning_boards_cards_lists_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_learning_board(request):
    user_workspace = request.user.learningboardworkspace
    new_board = LearningBoard.objects.create(
        name=request.data.get('name'),
        short_description=request.data.get('short_description'),
        workspace=user_workspace,
    )
    serializer = LearningBoardSerializer(new_board)
    return Response(serializer.data)


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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_teaching_subjects(request):
    user = request.user    

    if user.role =="Student":
        return Response({'error': 'You do not have permission to perform this action.'})
    subject_leader_subjects = Subject.objects.filter(subject_leader=user)
    
    if subject_leader_subjects.exists():
        serializer = SubjectSerializer(subject_leader_subjects, many=True)
        return Response(serializer.data)
    else:
        return JsonResponse({'no subjects': 'none'})
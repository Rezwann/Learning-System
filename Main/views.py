from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.db.models import Q
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardWorkspace, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem
from .models import CommunicationArea, Channel, Post, EngagementInstance
from .models import EHCP_View, EHCP_Interest, EHCP_Aspiration
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, SubjectSerializer, SubjectCategorySerializer, LearningBoardSerializer, LearningBoardCardSerializer
from .serializers import LearningBoardCardListSerializer, LearningBoardCardListItemSerializer
from .serializers import LearningBoardCardListItemSerializer
from .serializers import CommunicationAreaSerializer, ChannelSerializer, PostSerializer, LearningBoardWorkspaceSerializer
from .serializers import EngagementInstanceSerializer
from .serializers import EHCP_ViewSerializer, EHCP_InterestSerializer, EHCP_AspirationSerializer

from django.shortcuts import get_object_or_404
import math

@api_view(['GET'])
def get_custom_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_current_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        role = request.user.role      
        return JsonResponse({'username': username, 'role':role
        })
    else:
        return JsonResponse({'error': 'User is not authenticated'})

@api_view(['GET'])
def get_single_user(request):
    if request.user.is_authenticated:
        user = request.user
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'error': 'User is not authenticated'})

@api_view(['GET'])
def get_all_EHCP(request):
    if request.user.is_authenticated:
        user = request.user
        ehcp_view = EHCP_View.objects.get(user=user)
        ehcp_interest = EHCP_Interest.objects.get(user=user)
        ehcp_aspiration = EHCP_Aspiration.objects.get(user=user)
        
        ehcp_view_serializer = EHCP_ViewSerializer(ehcp_view)
        ehcp_interest_serializer = EHCP_InterestSerializer(ehcp_interest)
        ehcp_aspiration_serializer = EHCP_AspirationSerializer(ehcp_aspiration)
        
        return Response({
            'ehcp_view': ehcp_view_serializer.data,
            'ehcp_interest': ehcp_interest_serializer.data,
            'ehcp_aspiration': ehcp_aspiration_serializer.data
        })

@api_view(['POST'])
def get_student_EHCP(request):
    if request.user.is_authenticated:
        name = request.data.get('name')
        user = CustomUser.objects.get(username=name)            
        ehcp_view = EHCP_View.objects.get(user=user)
        ehcp_interest = EHCP_Interest.objects.get(user=user)
        ehcp_aspiration = EHCP_Aspiration.objects.get(user=user)        
        ehcp_view_serializer = EHCP_ViewSerializer(ehcp_view)
        ehcp_interest_serializer = EHCP_InterestSerializer(ehcp_interest)
        ehcp_aspiration_serializer = EHCP_AspirationSerializer(ehcp_aspiration)
        
        return Response({
            'ehcp_view': ehcp_view_serializer.data,
            'ehcp_interest': ehcp_interest_serializer.data,
            'ehcp_aspiration': ehcp_aspiration_serializer.data
        })

@api_view(['POST'])
def setEHCP(request):          
    studentname = request.data.get('studentname')
    ehcpInterest = request.data.get('ehcpInterest')
    ehcpAspiration = request.data.get('ehcpAspiration')
    ehcpView = request.data.get('ehcpView')

    user = CustomUser.objects.get(username=studentname)    
    user.hasEHCP = True    
    user.save()        
    
    ehcp_view, created = EHCP_View.objects.get_or_create(user=user)
    ehcp_view.student_views = ehcpView
    ehcp_view.save()
    
    ehcp_aspiration, created = EHCP_Aspiration.objects.get_or_create(user=user)
    ehcp_aspiration.student_aspirations = ehcpAspiration
    ehcp_aspiration.save()
    
    ehcp_interest, created = EHCP_Interest.objects.get_or_create(user=user)
    ehcp_interest.student_interests = ehcpInterest
    ehcp_interest.save()
    
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_engagement_instances(request):
    engagement_instances = EngagementInstance.objects.all()
    serializer = EngagementInstanceSerializer(engagement_instances, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_engagement_instance(request):
    username = request.user.username
    if request.user.is_authenticated:
        chosen_type = request.data.get('chosentype')
        custom_user = get_object_or_404(CustomUser, username=username)
        custom_user.desired_engagement_type = chosen_type
        custom_user.save()
        new_engagement_instance = EngagementInstance.objects.create(
            chosen_type=chosen_type, user=custom_user
        )
        serializer = EngagementInstanceSerializer(new_engagement_instance)
        return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
    final_group = "Medium"
    avg = (VM + NVM + L + EF) / 4
    if avg <= 20:
        final_group = "Very Low"
    elif avg <= 40:
        final_group = "Low"
    elif avg <= 60:
        final_group = "Medium"
    elif avg <= 80:
        final_group = "High"
    else:
        final_group = "Very High"
          
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
    user.vocabulary_sheet_group = final_group
    user.save()
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects(request):
    user = request.user
    subjects = Subject.objects.filter(Q(users=user))
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subject_categories(request):
    subject_categories = SubjectCategory.objects.all()
    serializer = SubjectCategorySerializer(subject_categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_communication_areas(request):
    communication_areas = CommunicationArea.objects.all()
    serializer = CommunicationAreaSerializer(communication_areas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_channels(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    cid = request.data.get('num')
    posts = Post.objects.filter(channel_id=cid)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_learning_workspace(request):
    user = request.user
    learning_workspace = LearningBoardWorkspace.objects.filter(user=user)
    serializer = LearningBoardWorkspaceSerializer(learning_workspace, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_learning_boards(request):
    user_workspace = request.user.learningboardworkspace
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    serializer = LearningBoardSerializer(learning_boards, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_learning_boards_cards(request):
    user_workspace = LearningBoardWorkspace.objects.get(user=request.user)
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    learning_boards_cards = LearningBoardCard.objects.filter(learning_board__in=learning_boards)
    serializer = LearningBoardCardSerializer(learning_boards_cards, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_learning_boards_cards_lists(request):
    user_workspace = LearningBoardWorkspace.objects.get(user=request.user)
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    learning_boards_cards_lists = LearningBoardCardList.objects.filter(learning_board_card__learning_board__in=learning_boards)
    serializer = LearningBoardCardListSerializer(learning_boards_cards_lists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_learning_boards_cards_lists_items(request):
    user_workspace = LearningBoardWorkspace.objects.get(user=request.user)
    learning_boards = LearningBoard.objects.filter(workspace=user_workspace)
    learning_boards_cards_lists_items = LearningBoardCardListItem.objects.filter(learning_board_card_list__learning_board_card__learning_board__in=learning_boards)
    serializer = LearningBoardCardListItemSerializer(learning_boards_cards_lists_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_learning_board_to_student(request):
    studentname = request.data.get('studentname')
    boardinfo = request.data.get('boardinfo')
    name = boardinfo.get('name')
    short_description = boardinfo.get('short_description')
    studentuser = CustomUser.objects.get(username=studentname)    
    studentuser_workspace = studentuser.learningboardworkspace
    new_board = LearningBoard.objects.create(
        name=name,
        short_description=short_description,
        workspace=studentuser_workspace,
        board_type = request.user.role
    )
    serializer = LearningBoardSerializer(new_board)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_learning_board(request):
    user_workspace = request.user.learningboardworkspace
    new_board = LearningBoard.objects.create(
        name=request.data.get('name'),
        short_description=request.data.get('short_description'),
        workspace=user_workspace,
        board_type = request.user.role
    )
    serializer = LearningBoardSerializer(new_board)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_learning_board(request):
    learningboard_id = request.data.get('num')
    learningboard = LearningBoard.objects.get(id=learningboard_id)
    learningboard.delete()
             
    return Response({'deleted:deleted'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_learning_board_card(request):
    learningboardcard_id = request.data.get('num')
    learningboardcard = LearningBoardCard.objects.get(id=learningboardcard_id)
    learningboardcard.delete()
             
    return Response({'deleted:deleted'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_my_teaching_subjects(request):
    user = request.user    
    subject_leader_subjects = Subject.objects.filter(subject_leader=user)    
    if subject_leader_subjects.exists():
        serializer = SubjectSerializer(subject_leader_subjects, many=True)
        return Response(serializer.data)
    else:
        return JsonResponse({'no subjects': 'none'})
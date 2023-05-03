from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Subject, SubjectCategory, LearningBoard, LearningBoardWorkspace, LearningBoardCard
from .models import LearningBoardCardList, LearningBoardCardListItem
from .models import CommunicationArea, Channel, Post, EngagementInstance
from .models import EHCP_View, EHCP_Interest, EHCP_Aspiration, EHCP_TeacherComment
from .models import DebatingArea, DebateSide, DebatingContribution, Opinion
from .serializers import CustomUserSerializer, SubjectSerializer, SubjectCategorySerializer, LearningBoardSerializer, LearningBoardCardSerializer
from .serializers import LearningBoardCardListSerializer, LearningBoardCardListItemSerializer
from .serializers import LearningBoardCardListItemSerializer
from .serializers import CommunicationAreaSerializer, ChannelSerializer, PostSerializer, LearningBoardWorkspaceSerializer
from .serializers import EngagementInstanceSerializer
from .serializers import EHCP_ViewSerializer, EHCP_InterestSerializer, EHCP_AspirationSerializer, EHCP_TeacherCommentSerializer
from .serializers import DebatingAreaSerializer, DebateSideSerializer, DebatingContributionSerializer, OpinionSerializer
from django.shortcuts import get_object_or_404
import math
from better_profanity import profanity
from textblob import TextBlob


# Section 1: Subjects and Neuro background - API Views:

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
    if not subject_categories:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = SubjectCategorySerializer(subject_categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_custom_users(request):
    try:
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=200)
    except:
        error_message = "Failed to retrieve custom users"
        return Response({"error": error_message}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_neurobackground(request):
    try:
        username = request.data.get('studentname')
        user = CustomUser.objects.get(username=username)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist.'}, status=500)
    except Exception as e:
        return Response({'error': str(e)})

# Section 2: Communication Area - API Views:

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_communication_areas(request):
    communication_areas = CommunicationArea.objects.all()
    if not communication_areas:
        return Response({"message": "No communication areas found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CommunicationAreaSerializer(communication_areas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_channels(request):
    channels = Channel.objects.all()
    if not channels:
        return Response({'message': 'No channels found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
        profanity.load_censor_words()
        content = request.data.get('content')        
        censored_content = profanity.censor(content)
        new_post = Post.objects.create(channel = channel_passed, author = user, content = censored_content)
        new_post.save()        
    return Response({'added:added'})

# Section 3: Debating - API Views:

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_debating_areas(request):
    debating_areas = DebatingArea.objects.all()
    if not debating_areas:
        return Response({'message': 'No debating areas.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DebatingAreaSerializer(debating_areas, many=True)
    debate_sides = [side for area in serializer.data for side in area['sides']]
    opinions = [opinion for area in serializer.data for side in area['sides'] for opinion in side['opinions']]
    data = {
        'debating_areas': serializer.data,
        'debate_sides': debate_sides,
        'opinions': opinions
    }
    return Response(data)

# Section 4: GET-Related Learning Workspace - API Views:

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

# Section 5: Non-GET-Related Learning Workspace - API Views:

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_learning_board(request):
    user_workspace = request.user.learningboardworkspace    
    name = request.data.get('name')
    short_description = request.data.get('short_description')
    
    if not name or not short_description:
        return Response({'message': 'Please provide both name and short_description.'}, status=status.HTTP_400_BAD_REQUEST)

    new_board = LearningBoard.objects.create(
        name=name,
        short_description=short_description,
        workspace=user_workspace,
        board_type=request.user.role
    )
    serializer = LearningBoardSerializer(new_board)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_learning_board(request):
    learningboard_id = request.data.get('num')
    try:
        learningboard = LearningBoard.objects.get(id=learningboard_id)
    except LearningBoard.DoesNotExist:
        return Response({'error': 'LearningBoard not found'}, status=status.HTTP_404_NOT_FOUND)
    learningboard.delete()
             
    return Response({'Board Deleted': 'Board Deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_learning_board_card(request):
    learningboardcard_id = request.data.get('num')
    try:
        learningboardcard = LearningBoardCard.objects.get(id=learningboardcard_id)
        learningboardcard.delete()
        return Response({'message': 'LearningBoardCard deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except LearningBoardCard.DoesNotExist:
        return Response({'error': 'LearningBoardCard not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_learning_board_card(request):
    learningboard_id = request.data.get('num')
    new_card_name = request.data.get('name')
    new_card_desc = request.data.get('description')
    try:
        learningboard = LearningBoard.objects.get(id=learningboard_id)
        new_card = LearningBoardCard.objects.create(
            name=new_card_name,
            short_description=new_card_desc,
            learning_board=learningboard
        )
        new_card.save()
        serializer = LearningBoardCardSerializer(new_card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except LearningBoard.DoesNotExist:
        return Response({'error': 'LearningBoard not found'}, status=status.HTTP_404_NOT_FOUND)

# Section 6: User (non-teacher), Engagement, and EHCP - API Views:

@api_view(['GET'])
def get_current_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        role = request.user.role
        dct = request.user.debate_contribution_target
        acd = request.user.averageCD
        return Response({'username': username, 'role': role, 'dct': dct, 'acd':acd})
    else:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_single_user(request):
    if request.user.is_authenticated:
        user = request.user
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'error': 'User is not authenticated'})

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_engagement_instances(request):
    engagement_instances = EngagementInstance.objects.all()
    if not engagement_instances:
        return Response({'error': 'No engagement instances exist.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EngagementInstanceSerializer(engagement_instances, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
        }, status=status.HTTP_200_OK)
        
# Section 7: Teacher - API Views:
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
        }, status=status.HTTP_200_OK)
        
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_student_neuro_background(request):
    expected_fields = ['VM', 'NVM', 'VP', 'VIPS', 'N', 'L', 'EF', 'VR']
    if not all(field in request.data for field in expected_fields):
        return Response({'detail': 'Missing one or more cognitive domain values.'}, status=status.HTTP_400_BAD_REQUEST)    
    VM = float(request.data.get('VM'))
    NVM = float(request.data.get('NVM'))
    VP = float(request.data.get('VP'))
    VIPS = float(request.data.get('VIPS'))
    N = float(request.data.get('N'))
    L = float(request.data.get('L'))
    EF =  float(request.data.get('EF'))
    VR = float(request.data.get('VR'))
    if any(val > 100 or val < 1 for val in [VM, NVM, VP, VIPS, N, L, EF, VR]):
        return Response({'detail': 'Invalid input.'}, status=status.HTTP_400_BAD_REQUEST)
    if any(val is None for val in [VM, NVM, VP, VIPS, N, L, EF, VR]):
        return Response({'detail': 'Invalid input.'}, status=status.HTTP_400_BAD_REQUEST)
    if None in [VM, NVM, VP, VIPS, N, L, EF, VR]:
        return Response({'detail': 'Invalid input.'}, status=status.HTTP_400_BAD_REQUEST)

    base_target = 5.0     
    addition_for_base_target = ((VM*0.2)+(NVM*0.05)+(VP*0.1)+(VIPS*0.1)+(N*0.05)+(L*0.15)
    +(EF*0.15) + (VR*0.3))    
    final_debate_target = base_target + (base_target*(2*(addition_for_base_target/100.0)))
    final_debate_target_rounded = math.ceil(final_debate_target)
    print(final_debate_target_rounded)
    
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
    return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subject_general_info(request):
    if request.user.is_authenticated:        
        subject_choices = dict(Subject.SUBJECT_CHOICES)
        year_choices = dict(Subject.YEAR_CHOICES)
        return Response({'subject_choices': subject_choices, 'year_choices': year_choices}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subject(request):
    user = request.user
    name = request.data.get('subjectchoice')
    categorychoice = request.data.get('categorychoice')
    yearchoice = request.data.get('yearchoice')
    
    valid_subject_choices = [choice[0] for choice in Subject.SUBJECT_CHOICES]
    if name not in valid_subject_choices:
        return Response({"error": "Invalid subject choice"}, status=status.HTTP_400_BAD_REQUEST)
    
    valid_year_choices = [choice[0] for choice in Subject.YEAR_CHOICES]
    if yearchoice not in valid_year_choices:
        return Response({"error": "Invalid year choice"}, status=status.HTTP_400_BAD_REQUEST)
    
    valid_category_choices = [choice[0] for choice in SubjectCategory.CATEGORY_CHOICES]
    if categorychoice not in valid_category_choices:
        return Response({"error": "Invalid category choice"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        category = SubjectCategory.objects.get(name=categorychoice)
    except SubjectCategory.DoesNotExist:
        return Response({"error": "Subject category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    category = SubjectCategory.objects.get(name=categorychoice)
    subject = Subject(name=name, category=category, year_group=yearchoice, 
    subject_leader=user)    
    subject.save()    
    subject.users.add(user)
    serializer = SubjectSerializer(subject)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
     
     
@api_view(['POST'])
def add_comment_EHCP(request):
    if request.user.is_authenticated:
        name = request.data.get('studentname')
        comment = request.data.get('ehcpComment')
        commentForSection = request.data.get('ehcpSection')
        student = CustomUser.objects.get(username=name)
        teacher = CustomUser.objects.get(username=request.user.username)        
        ehcp_view = EHCP_View.objects.get(user=student)        
        ehcp_interest = EHCP_Interest.objects.get(user=student)                
        ehcp_aspiration = EHCP_Aspiration.objects.get(user=student)                
        if not comment:
            return Response({'error': 'Comment cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        teacher_comment = EHCP_TeacherComment.objects.create(user=teacher, comment=comment)
        if commentForSection == 'views':
            ehcp_view = EHCP_View.objects.get(user=student)
            ehcp_view.teacher_comments.add(teacher_comment)
        elif commentForSection == 'interests':
            ehcp_interest = EHCP_Interest.objects.get(user=student)
            ehcp_interest.teacher_comments.add(teacher_comment)
        elif commentForSection == 'aspirations':
            ehcp_aspiration = EHCP_Aspiration.objects.get(user=student)
            ehcp_aspiration.teacher_comments.add(teacher_comment)
        else:
            return Response({'error': 'Invalid ehcpSection value'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EHCP_TeacherCommentSerializer(teacher_comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'error'}, status=status.HTTP_401_UNAUTHORIZED)
     
                                
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
     
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_learning_board_to_student(request):
    teacher_name = request.user.username
    studentname = request.data.get('studentname')
    boardinfo = request.data.get('boardinfo')
    name = boardinfo.get('name')
    short_description = boardinfo.get('short_description')
    try:
        studentuser = CustomUser.objects.get(username=studentname)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)    
    studentuser_workspace = studentuser.learningboardworkspace
    new_board = LearningBoard.objects.create(
        name=name + " - From Teacher: " + teacher_name,
        short_description=short_description,
        workspace=studentuser_workspace,
        board_type=request.user.role
    )
    serializer = LearningBoardSerializer(new_board)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_subject_area_members(request):
    users_to_remove = request.data.get('usersToRemove')
    print(users_to_remove)
    SAI = request.data.get('SAI')    
    subject_area = Subject.objects.get(id=SAI)
    for user_dict in users_to_remove:
        user_id = user_dict['id']
        username = user_dict['username']
        users = subject_area.users.filter(id=user_id, username=username)
        for user in users:
            subject_area.users.remove(user)    
    return JsonResponse({'none': 'none'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subject_area_members(request):
    users_to_add = request.data.get('usersToAdd')
    print(users_to_add)
    SAI = request.data.get('SAI')    
    subject_area = Subject.objects.get(id=SAI)        
    for user_dict in users_to_add:
        username = user_dict.get('username')
        user = CustomUser.objects.get(username=username)
        subject_area.users.add(user)        
    return JsonResponse({'none': 'none'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_debate_question(request):
    DebatingAreaID = request.data.get('area_id')    
    EditedQuestion = request.data.get('edited_question')    
    print(EditedQuestion)
    debating_area = DebatingArea.objects.get(id=DebatingAreaID)
    debating_area.debate_question = EditedQuestion
    debating_area.save()
    return JsonResponse({'none': 'none'})
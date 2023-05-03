from django.urls import path
from Main import views
urlpatterns = [
    
# Section 1 - Subjects and Neuro background API's
    path('', views.get_subjects, name='get_subjects'),
    path('subjectCategories/', views.get_subject_categories, name='subjectCategories'),
    path('getCustomUsers/', views.get_custom_users, name='getCustomUsers'),
    path('getUserNeurobackground/', views.get_user_neurobackground, name='getUserNeuroBackground'),    

# Section 2 - Communication Area API's  
    path('getCommunicationAreas/', views.get_communication_areas, name='getCommunicationAreas'),
    path('getCommunicationChannels/', views.get_channels, name='getCommunicationChannels'),    
    path('getCommunicationChannelPosts/', views.get_posts, name='getCommunicationChannelPosts'),
    path('addCommunicationChannelPost/', views.add_channel_post, name='addCommunicationChannelPost'),

# Section 3 - Debating API's  
    path('getDebatingAreas/', views.get_debating_areas, name="getDebatingAreas"),

# Section 4 - GET-Related Learning Workspace API's  
    path('getLearningWorkspace/', views.get_learning_workspace, name="getLearningWorkspace"),
    path('getLearningBoards/', views.get_learning_boards, name="getLearningBoards"),
    path('getLearningBoardsCards/', views.get_learning_boards_cards, name="getLearningBoardsCards"),
    path('getLearningBoardsCardsLists/', views.get_learning_boards_cards_lists, name="getLearningBoardsCardsLists"),
    path('getLearningBoardsCardsListsItems/', views.get_learning_boards_cards_lists_items, name="getLearningBoardsCardsListsItems"),

# Section 5 - Non-GET-Related Learning Workspace API's  
    path('addLearningBoard/', views.add_learning_board, name="addLearningBoard"),    
    path('deleteLearningBoard/', views.delete_learning_board, name="deleteLearningBoard"),
    path('deleteLearningBoardCard/', views.delete_learning_board_card, name="deleteLearningBoardCard"),
    path('addLearningBoardCard/', views.add_learning_board_card, name="addLearningBoardCard"),

# Section 6 - User (non-teacher), Engagement, and EHCP API's    
    path('getCurrentUser/', views.get_current_user, name="getCurrentUser"),
    path('getSingleUser/', views.get_single_user, name="getSingleUser"),
    path('postEngagementInstance/',views.post_engagement_instance, name="postEngagementInstance"),
    path('getEngagementInstances/',views.get_engagement_instances, name="getEngagementInstances"),
    path('getAllEHCP/', views.get_all_EHCP, name="getAllEHCP"),

# Section 7 - Teacher    
    path('getMyTeachingSubjects/', views.get_my_teaching_subjects, name="getMyTeachingSubjects"),
    path('updateStudentNeuroBackground/', views.update_student_neuro_background, name="updateStudentNeuroBackground"),
    path('addLearningBoardToStudent/', views.add_learning_board_to_student, name="addLearningBoardToStudent"),    
    path('setEHCP/',views.setEHCP, name="setEHCP"),
    
    path('getStudentEHCP/',views.get_student_EHCP, name="getStudentEHCP"),
    path('addCommentEHCP/',views.add_comment_EHCP, name="addCommentEHCP"),
    path('getGeneralSubjectInformation/', views.get_subject_general_info, name="getGeneralSubjectInformation"),
    path('createSubject/', views.create_subject, name="createSubject"),

    path('removeMembersFromSubjectArea/', views.remove_subject_area_members),
    path('addMembersToSubjectArea/', views.add_subject_area_members),    
    path('updateDebateQuestion/', views.update_debate_question)
]
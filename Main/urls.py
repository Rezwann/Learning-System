from django.urls import path

from Main import views

urlpatterns = [

# GET api's
    path('', views.get_subjects),
    path('subjectCategories/', views.get_subject_categories),
    path('getCustomUsers/', views.get_custom_users),
    path('getUserNeurobackground/', views.get_user_neurobackground),    
    path('getCommunicationAreas/', views.get_communication_areas),    
    path('getCommunicationChannels/', views.get_channels),    
    path('getCommunicationChannelPosts/', views.get_posts),
    path('addCommunicationChannelPost/', views.add_channel_post),

# Learning Board API's  
    path('getLearningWorkspace/', views.get_learning_workspace),
    path('getLearningBoards/', views.get_learning_boards),
    path('getLearningBoardsCards/', views.get_learning_boards_cards),
    path('getLearningBoardsCardsLists/', views.get_learning_boards_cards_lists),
    path('getLearningBoardsCardsListsItems/', views.get_learning_boards_cards_lists_items),

    path('addLearningBoard/', views.add_learning_board),    
    path('deleteLearningBoard/', views.delete_learning_board),
    path('deleteLearningBoardCard/', views.delete_learning_board_card),
    path('addLearningBoardCard/', views.add_learning_board_card),

# User API's    
    path('getCurrentUser/', views.get_current_user),
    path('getSingleUser/', views.get_single_user),
    path('postEngagementInstance/',views.post_engagement_instance),
    path('getEngagementInstances/',views.get_engagement_instances),
    path('getAllEHCP/', views.get_all_EHCP),

# Teacher    
    path('getMyTeachingSubjects/', views.get_my_teaching_subjects),
    path('updateStudentNeuroBackground/', views.update_student_neuro_background),
    path('addLearningBoardToStudent/', views.add_learning_board_to_student),    
    path('setEHCP/',views.setEHCP),
    path('getStudentEHCP/',views.get_student_EHCP),

]
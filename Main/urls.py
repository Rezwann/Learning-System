from django.urls import path

from Main import views

urlpatterns = [

# GET api's
    path('', views.get_subjects),
    path('subjectCategories/', views.get_subject_categories),
    path('getLearningBoards/', views.get_learning_boards),
    path('getLearningBoardsCards/', views.get_learning_boards_cards),
    path('getLearningBoardsCardsTags/', views.get_learning_boards_cards_tags),
    path('getLearningBoardsCardsLists/', views.get_learning_boards_cards_lists),
    path('getLearningBoardsCardsListsItems/', views.get_learning_boards_cards_lists_items),

    path('addLearningBoard/', views.add_learning_board),
    
    path('deleteLearningBoard/', views.delete_learning_board),
    path('deleteLearningBoardCard/', views.delete_learning_board_card),
    
    path('getCurrentUser/', views.get_current_user)
]
from django.urls import path

from Main import views

urlpatterns = [
    path('', views.get_subjects),
    path('subjectCategories/', views.get_subject_categories),
    path('getLearningBoards/', views.get_learning_boards),
    path('getLearningBoardsCards/', views.get_learning_boards_cards),
    path('getLearningBoardsCardsLists/', views.get_learning_boards_cards_lists),
    path('getLearningBoardsCardsListsItems/', views.get_learning_boards_cards_lists_items),
    
]
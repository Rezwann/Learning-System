from rest_framework.test import APIClient
from django.test import SimpleTestCase, tag
from django.urls import resolve, reverse
from Main.views import get_subjects, get_subject_categories, get_custom_users, get_user_neurobackground 
from Main.views import get_communication_areas, get_channels, get_posts, add_channel_post
from Main.views import get_debating_areas
from Main.views import get_learning_workspace, get_learning_boards, get_learning_boards_cards, get_learning_boards_cards_lists, get_learning_boards_cards_lists_items
from Main.views import add_learning_board, delete_learning_board, delete_learning_board_card, add_learning_board_card
from Main.views import get_current_user, get_single_user, post_engagement_instance, get_engagement_instances, get_all_EHCP
from Main.views import get_my_teaching_subjects, update_student_neuro_background, add_learning_board_to_student, setEHCP, get_student_EHCP, add_comment_EHCP, get_subject_general_info, create_subject
    
class TestUrls(SimpleTestCase):
    
    # ==== Testing Subjects and Neuro background - URL Testing:
        
    @tag('subjectsNeuro')
    def test_get_subjects_is_resolved(self):
        url = reverse('get_subjects')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_subjects)        
        
    @tag('subjectsNeuro')
    def test_subject_categories_is_resolved(self):
        url = reverse('subjectCategories')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_subject_categories)
    
    @tag('subjectsNeuro')    
    def test_get_custom_users_is_resolved(self):
        url = reverse('getCustomUsers')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_custom_users)
    
    @tag('subjectsNeuro')
    def test_get_user_neurobackground_is_resolved(self):
        url = reverse('getUserNeuroBackground')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_user_neurobackground)
        
    # ==== Testing Communication Area API's - URL Testing:
    
    @tag('communicationArea')
    def test_get_communication_areas_is_resolved(self):
        url = reverse('getCommunicationAreas')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_communication_areas)

    @tag('communicationArea')    
    def test_get_communication_channels_is_resolved(self):
        url = reverse('getCommunicationChannels')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_channels)
                
    @tag('communicationArea')        
    def test_get_communication_channel_posts_is_resolved(self):
        url = reverse('getCommunicationChannelPosts')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_posts)
        
    @tag('communicationArea')        
    def test_add_communication_channel_post_is_resolved(self):
        url = reverse('addCommunicationChannelPost')
        print(resolve(url))
        self.assertEquals(resolve(url).func,add_channel_post)    

    # ==== Testing Debating - URL Testing:
    
    @tag('debatingArea')
    def test_get_debating_areas_is_resolved(self):
        url = reverse('getDebatingAreas')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_debating_areas)        

    # ==== Testing GET-related Learning Workspace - URL Testing:
    
    @tag('getRelatedLearningWorkspace')
    def test_get_learning_workspace_is_resolved(self):
        url = reverse('getLearningWorkspace')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_learning_workspace)    
        
    @tag('getRelatedLearningWorkspace')
    def test_get_learning_boards_is_resolved(self):
        url = reverse('getLearningBoards')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_learning_boards)    
        
    @tag('getRelatedLearningWorkspace')
    def test_get_learning_boards_cards_is_resolved(self):
        url = reverse('getLearningBoardsCards')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_learning_boards_cards)    
        
    @tag('getRelatedLearningWorkspace')
    def test_get_learning_boards_cards_lists_is_resolved(self):
        url = reverse('getLearningBoardsCardsLists')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_learning_boards_cards_lists)    
        
    @tag('getRelatedLearningWorkspace')
    def test_get_learning_boards_cards_lists_items_is_resolved(self):
        url = reverse('getLearningBoardsCardsListsItems')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_learning_boards_cards_lists_items)    
        
    # ==== Testing Non-GET-related Learning Workspace - URL Testing:
    
    @tag('NongetRelatedLearningWorkspace')
    def test_add_learning_board_is_resolved(self):
        url = reverse('addLearningBoard')
        print(resolve(url))
        self.assertEquals(resolve(url).func,add_learning_board)      

    @tag('NongetRelatedLearningWorkspace')
    def test_delete_learning_board_is_resolved(self):
        url = reverse('deleteLearningBoard')
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_learning_board)      

    @tag('NongetRelatedLearningWorkspace')
    def test_delete_learning_board_card_is_resolved(self):
        url = reverse('deleteLearningBoardCard')
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_learning_board_card)      

    @tag('NongetRelatedLearningWorkspace')
    def test_add_learning_board_card_is_resolved(self):
        url = reverse('addLearningBoardCard')
        print(resolve(url))
        self.assertEquals(resolve(url).func,add_learning_board_card)      
        
    # ==== User (non-teacher), Engagement, and EHCP - URL Testing:    
        
    @tag('StudentEngagementEHCP')
    def test_get_current_user_is_resolved(self):
        url = reverse('getCurrentUser')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_current_user)      

    @tag('StudentEngagementEHCP')
    def test_get_single_user_is_resolved(self):
        url = reverse('getSingleUser')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_single_user)      

    @tag('StudentEngagementEHCP')
    def test_post_engagement_instance_is_resolved(self):
        url = reverse('postEngagementInstance')
        print(resolve(url))
        self.assertEquals(resolve(url).func,post_engagement_instance)      

    @tag('StudentEngagementEHCP')
    def test_get_engagement_instance_is_resolved(self):
        url = reverse('getEngagementInstances')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_engagement_instances)   
        
    @tag('StudentEngagementEHCP')
    def test_get_all_ehcp_resolved(self):
        url = reverse('getAllEHCP')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_all_EHCP)   

    # ==== Testing Teacher Subjects, NB, Workspace, EHCP, Subjects - URL Testing:
        
    @tag('TeacherMain')
    def test_get_my_teaching_subjects_is_resolved(self):
        url = reverse('getMyTeachingSubjects')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_my_teaching_subjects)      

    @tag('TeacherMain')
    def test_update_student_neuro_is_resolved(self):
        url = reverse('updateStudentNeuroBackground')
        print(resolve(url))
        self.assertEquals(resolve(url).func,update_student_neuro_background)      

    @tag('TeacherMain')
    def test_add_learning_board_to_student_is_resolved(self):
        url = reverse('addLearningBoardToStudent')
        print(resolve(url))
        self.assertEquals(resolve(url).func,add_learning_board_to_student)   
        
    @tag('TeacherMain')
    def test_set_student_ehcp_resolved(self):
        url = reverse('setEHCP')
        print(resolve(url))
        self.assertEquals(resolve(url).func,setEHCP)   
        
    @tag('TeacherMain')
    def test_get_student_ehcp_is_resolved(self):
        url = reverse('getStudentEHCP')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_student_EHCP)      

    @tag('TeacherMain')
    def test_add_comment_ehcp_is_resolved(self):
        url = reverse('addCommentEHCP')
        print(resolve(url))
        self.assertEquals(resolve(url).func,add_comment_EHCP)      

    @tag('TeacherMain')
    def test_get_general_subject_info_is_resolved(self):
        url = reverse('getGeneralSubjectInformation')
        print(resolve(url))
        self.assertEquals(resolve(url).func,get_subject_general_info)   
        
    @tag('TeacherMain')
    def test_create_subject_area_resolved(self):
        url = reverse('createSubject')
        print(resolve(url))
        self.assertEquals(resolve(url).func,create_subject)   


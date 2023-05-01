from django.test import TestCase, tag
from django.urls import resolve, reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.db.models import Q
from Main.models import CustomUser, Subject, SubjectCategory, Channel, Post, DebatingArea
from Main.models import DebateSide, LearningBoardWorkspace, LearningBoard, LearningBoardCard
from Main.models import LearningBoardCardList, LearningBoardCardListItem
from Main.models import EngagementInstance
from Main.models import EHCP_View, EHCP_Interest, EHCP_Aspiration
from Main.serializers import LearningBoardSerializer, EngagementInstanceSerializer, CustomUserSerializer, SubjectSerializer, SubjectCategorySerializer
from Main.serializers import EHCP_ViewSerializer, EHCP_InterestSerializer, EHCP_AspirationSerializer

class TestCases(TestCase):    
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testinghello', password='gardenflower55', email='checkingmyapp@gmail.com')
        SubjectCategory.objects.all().delete()
        self.client.force_authenticate(user=self.user)
        self.client.force_login(self.user)
        CAT = SubjectCategory.create(name='Core')        
        Subject.objects.create(name='Mathematics', category = CAT, year_group = 'Year 9',
                subject_leader=self.user)

        Subject.objects.create(name='English', category = CAT, year_group = 'Year 9',
                subject_leader=self.user)
    
    # ==== Testing related to Section 1 API Views (from my views.py):    
    # 1) Integration Test case: getting subjects associated with subject leader/users    
    @tag('Test1')
    def test_get_subjects(self):
        url = reverse('get_subjects')
        print(f'\nTest 1 - URL: {url}')
        response = self.client.get(url)
        subjects = Subject.objects.filter(Q(subject_leader=self.user))
        print("Test 1 - Subjects that test user is associated with:")
        for subject in subjects:
            print(f"- {subject.name} {subject.subject_code} {subject.year_group}")        
        # Only show error if my test gives wrong output
        self.assertTrue(len(subjects) > 0, 'No subjects associated with the user')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'\nTest 1 - Response code: {response.status_code}')

    # 2) Unit Test case: creating and listing individual subject categories  
    @tag('Test2')          
    def test_get_and_create_subject_categories(self):
        url = reverse('subjectCategories')
        print(f'\nTest 2 - URL: {url}')
        response = self.client.get(url)
        SubjectCategory.objects.all().delete()    
        category_names = ['Modern Foreign Languages', 'Humanity', 'Arts', 'Technical']
        for name in category_names:
            SubjectCategory.create(name) 
        AllSubjectCategories = SubjectCategory.objects.filter()            
        print("Test 2 - Subjects categories created")
        for category in AllSubjectCategories:
            print(f"- {category.name}")                                  
        if len(category_names) > 0:
                self.assertEqual(SubjectCategory.objects.count(), len(category_names))
                for category in AllSubjectCategories:
                    self.assertIn(category.name, category_names)
        else:
                self.assertEqual(len(AllSubjectCategories), 0)                
        if not AllSubjectCategories:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        else:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'\nTest 2 - Response code: {response.status_code}')

    # 3) Unit Test case: getting custom users     
    @tag('Test3')          
    def test_get_custom_users_is_resolved(self):
        url = reverse('getCustomUsers')
        print(f'\nTest 3 - URL: {url}')
        CustomUser.objects.create(username='Carlos', email='Carlos5550@example.com',password='gardenflower55')
        CustomUser.objects.create(username='Robert', email='Robert345@example.com', password='gardenflower55')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        actual_data = response.json()
        print(f'\nTest 3 - custom users obtained')
        for user in actual_data:
            print("Username:", user["username"])
        self.assertEqual(len(actual_data), 3) # include my customUser in setUp()
        print(f'\nTest 3 - Response code: {response.status_code}')

    # 4) Unit Test case: getting neurobackground for only existing students   
    @tag('Test4')           
    def test_get_user_neurobackground_is_resolved(self):
        url = reverse('getUserNeuroBackground')
        print(f'\nTest 4 - URL: {url}')
        CustomUser.objects.create(username='testuser', email='testuser@gmail.com', password='harry545')
        valid_data = {'studentname': 'testuser'}
        response = self.client.post(url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'\nTest 4 - Valid Data - Response code: {response.status_code}')

        invalid_data = {'studentname': 'thisuserdoesnotexist'}        
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'User does not exist.')
        print(f'\nTest 4 - Invalid Data - Response code: {response.status_code}')
        
    # ==== Testing related to Section 2 API Views (from my views.py):    
    # 5) Integration Test case: getting subject-specific communication areas that
    # are made as a result of two Subject (models) creation in my setUp()
    @tag('Test5')
    def test_get_communication_areas(self):
        url = reverse('getCommunicationAreas')
        print(f'\nTest 5 - URL: {url}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        print(f'\nTest 5 - Communication Areas made - Response code: {response.status_code}')

        if response.status_code == status.HTTP_200_OK:
            self.assertIsInstance(response.data, list)
            self.assertGreater(len(response.data), 0)
            print(f'\nTest 5 - Found subject-specific Communication Areas:')
            for area in response.data:
                self.assertIn('id', area)
                self.assertIsInstance(area['id'], int)
                self.assertIn('name', area)
                self.assertIsInstance(area['name'], str)                
                print(area)
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertIn('message', response.data)
            self.assertEqual(response.data['message'], 'No communication areas found ')
                        
    # 6) Integration Test case: getting communication channels for existing subjects and areas
    @tag('Test6')
    def test_get_communication_channels(self):
        url = reverse('getCommunicationChannels')
        print(f'\nTest 6 - URL: {url}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        subjects = Subject.objects.filter(Q(name__icontains='Mathematics') | Q(name__icontains='English'))
        for subject in subjects:
            subject_channels = [channel for channel in data if subject.name.lower() in channel['name'].lower()]
            self.assertGreater(len(subject_channels), 0)            
            # Only existing two existing subjects' channels should be listed
            if len(subject_channels) > 0:
                print(f"Test 6 - Found Channels for {subject.name}:")
                for channel in subject_channels:
                    print(channel['name'], end=' ')

    # 7) Integration Test Case: making Posts (model) and getting channel-specific instances
    @tag('Test7')
    def test_get_channel_specific_post(self):
        channels = Channel.objects.all()
        for channel in channels:
            Post.objects.create(channel=channel, author=self.user, content="Test Post Content")
        url = reverse('getCommunicationChannelPosts')
        print(f'\nTest 7 - URL: {url}')
        for channel in channels:
            data = {'num': channel.id}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertGreater(len(response.data), 0)
            for post in response.data:
                self.assertEqual(post['channel_id'], channel.id)
                self.assertEqual(post['author'], self.user.id)
                self.assertEqual(post['content'], 'Test Post Content')
        print(f'\nTest 7 - Response code: {response.status_code}')
        
    # ==== Testing related to Section 3 API Views (from my views.py):            
    # 8) Integration Test Case: getting subject-specific debating areas and default sides resulting
    @tag('Test8')
    def test_get_debating_areas(self):
        url = reverse('getDebatingAreas')
        print(f'\nTest 8 - URL: {url}')
        response = self.client.get(url)
        data_response = response.json()        
        self.assertEqual(len(data_response['debating_areas']), 2) # Mathematics, English from my setUp()       
        for area in data_response['debating_areas']:
            print(f"Test 8 -Debating area: {area['name']}")
            self.assertTrue('name' in area)
            self.assertTrue('debate_question' in area)
            self.assertEqual(len(area['sides']), 3) # Yes, No, Unsure
            for side in area['sides']:
                print(f"Side name: {side['side_name']}", end=' ')
                self.assertTrue('side_name' in side)          
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        print(f'\nTest 8 - Response code: {response.status_code}')
        
    # ==== Testing related to Section 4 API Views (from my views.py):        
    # 9) Unit Test Case: checking that a specific user automatically has one learning
    # workspace (model) created and available to them
    @tag('Test9')
    def test_get_users_learning_workspace(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('getLearningWorkspace'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.user.username, response.data[0]['name'])
        self.assertIn('Workspace', response.data[0]['name'])        
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        if workspace is not None:
            self.assertIsNotNone(workspace)
            print("Test 9 - Workspace found for test user:")
            print(workspace.name)
            print(f'\nTest 9 - Response code: {response.status_code}')
        else:
            print(f"Error: Failed - no workspace for {self.username}")
            
    # 10) Unit Test Case: creating and getting learning boards associated with user's workspace
    @tag('Test10')
    def test_get_learning_boards(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        LearningBoard.objects.create(name='Test Board', workspace=workspace)        
        self.client.force_login(self.user)
        response = self.client.get(reverse('getLearningBoards'))        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[1]['name'], 'Test Board')
        print(f'\nTest 10 - Response code: {response.status_code}')
        
    # 11) Unit Test Case: creating and getting learning board cards associated 
    # with a specific user's workspace
    @tag('Test11')
    def test_get_learning_board_cards(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Board', workspace=workspace)
        card1 = LearningBoardCard.objects.create(name='Card 1', learning_board=board)
        card2 = LearningBoardCard.objects.create(name='Card 2', learning_board=board)
        card3 = LearningBoardCard.objects.create(name='Card 3', learning_board=board)
        self.client.force_login(self.user)
        response = self.client.get(reverse('getLearningBoardsCards'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'Card 1')
        self.assertEqual(response.data[1]['name'], 'Card 2')
        self.assertEqual(response.data[2]['name'], 'Card 3')        
        print(f"\n Test 11- The following test cards were added to test user - {self.user}'s workspace ({workspace.name} - Board called: {board.name}):")
        print(f"- {card1.name}, {card2.name}, {card3.name}")
        print(f'\nTest 11 - Response code: {response.status_code}')
        
    # 12) Integration Test Case: creating and getting cards, card list, and list item
    @tag('Test12')
    def test_get_learning_boards_cards_lists(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Board', workspace=workspace)
        card1 = LearningBoardCard.objects.create(name='Card 1', learning_board=board)
        card_list = LearningBoardCardList.objects.create(
            learning_board_card=card1, name=f'Card List for {card1.name}',
            short_description=f'Card List for {card1.name} Description')
                
        item1 = LearningBoardCardListItem.objects.create(
            learning_board_card_list=card_list, name=f'Item 1 for {card1.name}')
        item2 = LearningBoardCardListItem.objects.create(
            learning_board_card_list=card_list, name=f'Item 2 for {card1.name}')

        card_list.items.add(item1, item2) 
        self.client.force_login(self.user)
        response = self.client.get(reverse('getLearningBoardsCardsLists'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'\nTest 12 - Response code: {response.status_code}')
        
    # ==== Testing related to Section 5 API Views (from my views.py):    
    # 13) Unit Test Case: Adding a learning board with all fields
    @tag('Test13')
    def test_add_learning_board(self):
        url = reverse('addLearningBoard')
        data = {
            'name': 'Test Board',
            'short_description': 'Test Board Description'
        }
        response = self.client.post(url, data, format='json')
        board = LearningBoard.objects.get(name='Test Board')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, LearningBoardSerializer(board).data)
        print(f'\nTest 13 - Response code: {response.status_code}')

 
    # 14) Unit Test Case: Adding a Learning Board (no data, only desc, only name, all data)
    @tag('Test14')
    def test_add_learning_board_missing_fields(self):
        url = reverse('addLearningBoard')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Please provide both name and short_description.'})    
        print(f'\nTest 14 - No data - Response code: {response.status_code}')        
        data = {'short_description': 'Test Board Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Please provide both name and short_description.'})    
        print(f'\nTest 14 - Only Description - Response code: {response.status_code}')        
        data = {'name': 'Test Board'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Please provide both name and short_description.'})    
        print(f'\nTest 14 - Only Name - Response code: {response.status_code}')        
        data = {'name': 'Test Board', 'short_description': 'Test Board Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Board')
        self.assertEqual(response.data['short_description'], 'Test Board Description')
        self.assertEqual(response.data['board_type'], self.user.role)
        print(f'\nTest 14 - Both fields - Response code: {response.status_code}')        



    # 15) Unit Test Case: deleting a board when one with the given ID exists
    @tag('Test15')
    def test_delete_board_normal(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Board', workspace=workspace)        
        self.client.force_login(self.user)
        url = reverse('deleteLearningBoard')
        data = {'num': board.id}
        response = self.client.post(url, data=data)        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(LearningBoard.DoesNotExist):
            LearningBoard.objects.get(id=board.id)
        print(f"\nTest 15 - Board deleted successfully. Response code: {response.status_code}")







    # 16) Unit Test Case: deleting a board when one with the given ID does not exist
    @tag('Test16')
    def test_delete_board_no_id(self):
        self.client.force_login(self.user)
        url = reverse('deleteLearningBoard')
        data = {'num': 5000}
        response = self.client.post(url, data=data)            
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'LearningBoard not found'})
        print(f"\nTest 16 - Board not found. Response code: {response.status_code}")










    # 17) Unit Test Case: deleting an existing board's card
    @tag('Test17')
    def test_delete_learning_board_card_is_resolved(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Board', workspace=workspace)
        card = LearningBoardCard.objects.create(name='Test Card', learning_board=board)
        url_delete_card = reverse('deleteLearningBoardCard')                       
        self.client.force_login(self.user)
        data = {'num': card.id}
        response = self.client.post(url_delete_card, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(LearningBoardCard.objects.filter(id=card.id).exists())
        self.assertEqual(response.data, {'message': 'LearningBoardCard deleted successfully'})
        print(f"\nTest 17 - Successfuly deleted board card. Response code: {response.status_code}")

    # 18) Unit Test Case: deleting a non-existent board card
    @tag('Test18')
    def test_delete_learning_board_card_failing(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Board', workspace=workspace)
        self.client.force_login(self.user)
        url_delete_card = reverse('deleteLearningBoardCard')                       
        data = {'num': 1000}
        response = self.client.post(url_delete_card, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'LearningBoardCard not found'})
        print(f"\nTest 18 - Failure to delete board card. Response code: {response.status_code}")

    # 19) Unit Test Case: adding a learning board card to existing board
    @tag('Test19')
    def test_add_learning_board_card_is_resolved(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Board', workspace=workspace)
        self.client.force_login(self.user)
        url_add_card = reverse('addLearningBoardCard')
        data = {'num': board.id, 'name': 'New Card', 'description': 'New Card Description'}
        response = self.client.post(url_add_card, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(LearningBoardCard.objects.filter(name='New Card', learning_board=board).exists())
        self.assertEqual(response.data['name'], 'New Card')
        self.assertEqual(response.data['short_description'], 'New Card Description')
        print(f"\nTest 19 - Successfuly added board card. Response code: {response.status_code}")

    # 20) Unit Test Case: trying to add a learning board card to non-existent board
    @tag('Test20')
    def test_add_learning_board_card_failling(self):
        self.client.force_login(self.user)
        url_add_card = reverse('addLearningBoardCard')
        data = {'num': 5000, 'name': 'New Card', 'description': 'New Card Description'}
        response = self.client.post(url_add_card, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'LearningBoard not found'})        
        print(f"\nTest 20 - Failure to add board card. Response code: {response.status_code}")
        
    # ==== Testing related to Section 5 API Views (from my views.py):    
    # 21) Unit/Security Test Case: getting user information while not authenticated
    @tag('Test21')
    def test_user_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('getCurrentUser'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
        print(f"\nTest 21 - Failure to get current user. Response code: {response.status_code}")

    # 22) Unit/Security Test Case: getting user information with authentication in setUp()
    @tag('Test22')
    def test_user_authenticated(self):
        url = reverse('getCurrentUser')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"\nTest 22 - Obtained current user. Response code: {response.status_code}")

    # 23) Unit Test Case: setting different engagement types
    @tag('Test23')
    def test_post_engagement_instance(self):
        url = reverse('postEngagementInstance')
        data = {'chosentype': 'Looking to participate'}
        self.client.force_login(self.user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['chosen_type'], 'Looking to participate')
        self.assertEqual(response.data['user']['id'], self.user.id)
        print(f"\nTest 23 - Successfully post engagement instance. Response code: {response.status_code}")
        data = {'chosentype': 'Looking to uniquely contribute in class'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['chosen_type'], 'Looking to uniquely contribute in class')
        self.assertEqual(response.data['user']['id'], self.user.id)
        print(f"\nTest 23 - Successfully post engagement instance. Response code: {response.status_code}")

    # 24) Unit Test Case: getting engagement instances (student's selection of preference)
    @tag('Test24')
    def test_get_engagement_instances(self):
        self.client.force_login(self.user)
        url = reverse('getEngagementInstances')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        engagement_instances = EngagementInstance.objects.all()
        serializer = EngagementInstanceSerializer(engagement_instances, many=True)
        self.assertEqual(response.data, serializer.data)
        print(f"\nTest 24 - Successfully obtained associated engagement instances. Response code: {response.status_code}")

    # 25) Integration Test Case: getting objects concerning EHCP (views/interests/aspirations)
    # that belong to a specific user
    @tag('Test25')
    def test_get_all_EHCP(self):
        ehcp_view = EHCP_View.objects.get(user=self.user)
        ehcp_interest = EHCP_Interest.objects.get(user=self.user)
        ehcp_aspiration = EHCP_Aspiration.objects.get(user=self.user)
        response = self.client.get(reverse('getAllEHCP'))
        ehcp_view_serializer = EHCP_ViewSerializer(ehcp_view)
        ehcp_interest_serializer = EHCP_InterestSerializer(ehcp_interest)
        ehcp_aspiration_serializer = EHCP_AspirationSerializer(ehcp_aspiration)
        expected_data = {
            'ehcp_view': ehcp_view_serializer.data,
            'ehcp_interest': ehcp_interest_serializer.data,
            'ehcp_aspiration': ehcp_aspiration_serializer.data
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        print(f"\nTest 25 - Successfully obtained user-associated EHCP object(s). Response code: {response.status_code}")
        
    # 26) Unit Test Case: updating cognitive domain level values of speciifc user with valid float data (1 to 100)
    @tag('Test26')
    def test_update_student_neuro_background_valid_data(self):
        url = reverse('updateStudentNeuroBackground')
        data = {
            'studentname': 'testinghello', 'VM': 75.0, 'NVM': 70.0, 'VP': 80.0, 'VIPS': 60.0, 'N': 50.0, 
            'L': 65.0, 'EF': 85.0, 'VR': 90.0,}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['verbal_memory_level'], 75.0)
        self.assertEqual(response.data['non_verbal_memory_level'], 70.0)
        self.assertEqual(response.data['visual_perception_level'], 80.0)
        self.assertEqual(response.data['visual_information_processing_speed_level'], 60.0)
        self.assertEqual(response.data['numeracy_level'], 50.0)
        self.assertEqual(response.data['literacy_level'], 65.0)
        self.assertEqual(response.data['executive_function_level'], 85.0)
        self.assertEqual(response.data['verbal_reasoning_level'], 90.0)
        print(f"\nTest 26 - Successfully updating neuro background. Response code: {response.status_code}")

    # 27) Unit Test Case: updating cognitive domain level values of speciifc user 
    # with invalid data (float beyond 100) to ensure correct output/response
    @tag('Test27')
    def test_update_student_neuro_background_invalid_range(self):
        url = reverse('updateStudentNeuroBackground')
        data = {
            'studentname': 'testinghello','VM': 110.0,'NVM': 500.0,'VP': 240.0,'VIPS': 60.0,
            'N': 45.0,'L': 65.0,'EF': 85.0,'VR': 90.0,}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Invalid input.'})
        print(f"\nTest 27 - Invalid range when updating neuro background. Response code: {response.status_code}")

    # 28) Unit Test Case: updating cognitive domain level values of speciifc user 
    # with certain CD values missing altogether to ensure correct output/response  
    @tag('Test28')                      
    def test_update_student_neuro_background_missing_CD(self):
        url = reverse('updateStudentNeuroBackground')
        data = {
            'studentname': 'testinghello','VM': 110.0,'NVM': 500.0,'N': 45.0,'L': 65.0,'EF': 85.0,'VR': 90.0,}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Missing one or more cognitive domain values.'})
        print(f"\nTest 28 - Losing or not given all CD values when updating neuro background. Response code: {response.status_code}")

    # 29) Unit Test Case: adding to an existing student's learning board (as a teacher) 
    @tag('Test29')
    def test_add_learning_board_to_valid_student(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Learning Board', short_description='This is a test learning board',workspace=workspace)
        self.client.force_login(self.user)
        url = reverse('addLearningBoardToStudent')
        data = {
            'studentname': f'{self.user.username}',
            'boardinfo': {'name': f'{board.name}','short_description': f'{board.short_description}'}
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Learning Board')
        self.assertEqual(response.data['short_description'], 'This is a test learning board')
        self.assertTrue(LearningBoard.objects.filter(name='Test Learning Board', workspace=self.user.learningboardworkspace).exists())
        print(f"\nTest 29 - Successfully added learning board to existing student. Response code: {response.status_code}")

    # 30) Unit Test Case: trying to add to non-existent student user's learning board
    @tag('Test30')
    def test_add_learning_board_to_nonexistent_student(self):
        workspace = LearningBoardWorkspace.objects.get(user=self.user)
        board = LearningBoard.objects.create(name='Test Board', short_description='desc',workspace=workspace)
        self.client.force_login(self.user)
        url = reverse('addLearningBoardToStudent')
        data = {
            'studentname': 'nonexistent_user',
            'boardinfo': {'name': f'{board.name}','short_description': f'{board.short_description}'}
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'User does not exist'})
        self.assertFalse(LearningBoard.objects.filter(name='Test Learning Board', workspace=self.user.learningboardworkspace).exists())
        print(f"\nTest 30 - Failed to add learning board to non-existent student. Response code: {response.status_code}")

    # 31) Integration Test Case: setting student's EHCP objects (teacher task)
    @tag('Test31')
    def test_set_EHCP_is_resolved(self):
        url = reverse('setEHCP')
        data = {'studentname': f'{self.user.username}','ehcpInterest': "TEST - Student's Interests from EHCP",
            'ehcpAspiration': "TEST - Student's Aspirations from EHCP",'ehcpView': "TEST - Student's Views from EHCP"}
        response = self.client.post(url, data=data)         
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        ehcp_view = EHCP_View.objects.get(user=self.user)
        ehcp_interest = EHCP_Interest.objects.get(user=self.user)
        ehcp_aspiration = EHCP_Aspiration.objects.get(user=self.user)                
        self.assertTrue(response.data['hasEHCP'])
        self.assertEqual(ehcp_view.student_views, "TEST - Student's Views from EHCP")
        self.assertEqual(ehcp_aspiration.student_aspirations, "TEST - Student's Aspirations from EHCP")
        self.assertEqual(ehcp_interest.student_interests, "TEST - Student's Interests from EHCP")
        print(f"\nTest 31 - Successfully setting student-specific EHCP objects. Response code: {response.status_code}")

    # 32) Integration Test Case: getting default EHCP objects and expecting default values
    # mentioning that EHCP has not been setup
    @tag('Test32')
    def test_get_student_EHCP_is_resolved(self):
        self.client.force_login(self.user)
        url = reverse('getStudentEHCP')        
        response = self.client.post(url, {'name': self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ehcp_view']['student_views'], "Student's Views from EHCP - not setup yet")
        self.assertEqual(response.data['ehcp_interest']['student_interests'], "Student's Interests from EHCP - not setup yet")
        self.assertEqual(response.data['ehcp_aspiration']['student_aspirations'], "Student's Aspirations from EHCP - not setup yet")
        print(f"\nTest 32 - Successfully getting default 'not setup yet' values in EHCP Objects. Response code: {response.status_code}")

    # 33) Unit Test Case: adding a teacher comment to EHCP section with valid data
    @tag('Test33')
    def test_add_comment_EHCP_is_resolved(self):
        self.client.force_login(self.user)
        url = reverse('addCommentEHCP')
        data = {'studentname': f'{self.user.username}','ehcpComment': "This is a test comment.",'ehcpSection': "views"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], "This is a test comment.")
        print(f"\nTest 33 - Successfully adding teacher comment to EHCP section. Response code: {response.status_code}")

    # 34) Unit Test Case: trying to add a teacher comment to invalid EHCP section
    @tag('Test34')
    def test_add_comment_EHCP_invalid_EHCP_section(self):
        self.client.force_login(self.user)
        url = reverse('addCommentEHCP')
        data = {'studentname': f'{self.user.username}','ehcpComment': "This is a test comment.",
            'ehcpSection': "invalid_section"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"\nTest 34 - Failure to add teacher comment (invalid EHCP section). Response code: {response.status_code}")

    # 35) Unit Test Case: trying to add teacher comment while no comment is entered
    @tag('Test35')
    def test_add_comment_EHCP_empty_comment(self):
        self.client.force_login(self.user)
        url = reverse('addCommentEHCP')
        data = {'studentname': f'{self.user.username}','ehcpComment': "",'ehcpSection': "views"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Comment cannot be empty")
        print(f"\nTest 35 - Failure to add teacher comment (empty EHCP comment content). Response code: {response.status_code}")

    # 36) Unit Test Case: getting subject + year choices, and checking that setUp() Subject instances used these values
    @tag('Test36')
    def test_get_subject_general_info(self):
        url = reverse('getGeneralSubjectInformation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_subject_choices = {'Science': 'Science','English': 'English','Mathematics': 'Mathematics',
            'French': 'French','German': 'German','Spanish': 'Spanish','Mandarin': 'Mandarin',
            'Japanese': 'Japanese','History': 'History','Geography': 'Geography',
            'Economics': 'Economics','Psychology': 'Psychology','Sociology': 'Sociology',
            'Music': 'Music','Drama': 'Drama','Dance': 'Dance','Computing': 'Computing','Business': 'Business'
        }
        expected_year_choices = {
            'Year 7': 'Year 7','Year 8': 'Year 8','Year 9': 'Year 9','Year 10': 'Year 10','Year 11': 'Year 11'}

        data = response.json()
        self.assertEqual(data['subject_choices'], expected_subject_choices)
        self.assertEqual(data['year_choices'], expected_year_choices)        
        subjects = Subject.objects.filter(subject_leader=self.user)
        for subject in subjects:
            self.assertIn(subject.name, expected_subject_choices)
            self.assertIn(subject.year_group, expected_year_choices)
        print(f"\nTest 36 - Successfully getting subject and year choices and valid subject "
            f"choice and year group in two Subject instances."
            f"\nResponse code: {response.status_code}")
        
        
    # 37) Integration Test Case: creating a subject with valid data, including
    # existing subject category instance, and both subject + year choice in my models.py
    @tag('Test37')
    def test_create_subject_is_resolved(self):
        SubjectCategory.create(name='Arts')        
        self.client.force_login(self.user)
        url = reverse('createSubject')
        data = {'subjectchoice': 'Mathematics','categorychoice': 'Arts','yearchoice': 'Year 11'}
        response = self.client.post(url, data=data)        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Mathematics')
        self.assertEqual(response.data['category_name'], 'Arts')
        self.assertEqual(response.data['year_group'], 'Year 11')
        print(f"\nTest 37 - Successfully creating a subject (teacher task). Response code: {response.status_code}")

    # 38) Integration Test Case: trying to create a subject with invalid subject choice     
    @tag('Test38')   
    def test_create_subject_invalid_subject_choice(self):
        SubjectCategory.create(name='Arts')        
        self.client.force_login(self.user)
        url = reverse('createSubject')
        data = {'subjectchoice': 'invalid_subject','categorychoice': 'Arts','yearchoice': 'Year 11'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid subject choice')
        print(f"\nTest 38 - Failure to create a subject (invalid subject choice). Response code: {response.status_code}")

    # 39) Integration Test Case: trying to create a subject with invalid year choice        
    @tag('Test39')        
    def test_create_subject_invalid_year_choice(self):
        SubjectCategory.create(name='Arts')        
        self.client.force_login(self.user)
        url = reverse('createSubject')
        data = {'subjectchoice': 'Mathematics','categorychoice': 'Arts','yearchoice': 'invalid_year'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid year choice')
        print(f"\nTest 39 - Failure to create a subject (invalid year choice). Response code: {response.status_code}")

    # 40) Integration Test Case: trying to create a subject with non-existent subjectCategory  
    @tag('Test40')     
    def test_create_subject_nonexistent_subject_category(self):
        SubjectCategory.create(name='Arts') # <-- making Arts (not Technical) to trigger response
        self.client.force_login(self.user)
        url = reverse('createSubject')
        data = {'subjectchoice': 'Mathematics',
            'categorychoice': 'Technical', # Technical SubjectCategory not made like Arts
            'yearchoice': 'Year 11'}        
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Subject category does not exist')
        print(f"\nTest 40 - Failure to create a subject (subjectCategory not created yet). Response code: {response.status_code}")
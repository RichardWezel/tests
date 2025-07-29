from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from forum_app.models import Question, Answer, Like
from forum_app.api.serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from rest_framework.authtoken.models import Token

class QuestionTests(APITestCase):

   def setUp(self):
      self.user = User.objects.create_user(username='testuser', password='testpassword')
      self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')

      self.token = Token.objects.create(user=self.user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

   def test_post_question_cretae_status(self):
      # ARRANGE
      url = reverse('question-list')
      data = {
            'title': 'Question1',
            'content': 'This is a new question.',
            'author': self.user.id,
            'category': 'frontend'
         }
      
      # ACT
      response = self.client.post(url, data, format='json')

      # ASSERT
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_detail_post_question_toolong_category(self):
      # ARRANGE
      url = reverse('question-list')
      data = {
            'title': 'Question1',
            'content': 'This is a new question.',
            'author': self.user.id,
            'category': 'frontendkjjskdjfjsdjfhsdhgdfhogfjd'
         }
      # ACT
      response = self.client.post(url, data, format='json')

      # ASSERT
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      # self.assertIn('category', response.data)

   def test_detail_question(self):
      # ARRANGE
      url = reverse('question-detail', kwargs={'pk': self.question.id})

      # ACT
      response = self.client.get(url)
      expected_data = QuestionSerializer(self.question).data

      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertDictEqual(response.data, expected_data)
      self.assertJSONEqual(response.content, expected_data)
      self.assertContains(response, 'title')

      self.assertEqual(Question.objects.count(), 1)
      self.assertEqual(Question.objects.get().author, self.user)


   def test_create_question(self):
    # ARRANGE
    url = reverse('question-list')
    data = {
        'title': 'Wie funktioniert DRF?',
        'content': 'Ich will wissen, wie das mit den Serializern geht.',
        'category': 'backend',
        'author': self.user.id  # optional, falls durch Token gesetzt auch weglassbar
    }

    # ACT
    response = self.client.post(url, data, format='json')

    # ASSERT
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Question.objects.count(), 2)  # vorher 1 in setUp
    self.assertEqual(Question.objects.last().title, 'Wie funktioniert DRF?')
 

   
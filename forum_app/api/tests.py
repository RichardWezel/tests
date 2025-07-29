from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from forum_app.models import Question, Answer, Like
from forum_app.api.serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from rest_framework.authtoken.models import Token

class LikeTests(APITestCase):

   def test_get_like(self):
      url = 'http://127.0.0.1:8000/api/forum/likes/'
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

class QuestionTests(APITestCase):

   def setUp(self):
      self.user = User.objects.create_user(username='testuser', password='testpassword')
      self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user, category='frontend')

      self.token = Token.objects.create(user=self.user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

   def test_detail_post_question(self):
      url = reverse('question-list')
      data = {
            'title': 'Question1',
            'content': 'This is a new question.',
            'author': self.user.id,
            'category': 'frontend'
         }
   
      response = self.client.post(url, data, format='json')

      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_detail_question(self):
      url = reverse('question-detail', kwargs={'pk': self.question.id})
      response = self.client.get(url)
      expected_data = QuestionSerializer(self.question).data

      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertDictEqual(response.data, expected_data)
      self.assertJSONEqual(response.content, expected_data)
      self.assertContains(response, 'title')

      self.assertEqual(Question.objects.count(), 1)
      self.assertEqual(Question.objects.get().author, self.user)

   

   
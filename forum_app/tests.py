from rest_framework.test import APITestCase

class AccountTests(APITestCase):
    def test_account_creation(self):
        url = '/api/accounts/'
        data = {
            'username': 'testuser',
            'email': 'test@email.de',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        
        
        
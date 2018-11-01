from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                response_empty_username = client.post('/register', data={})
                response_empty_password = client.post('/register', data={'username': 'test'})

                self.assertEqual(response_empty_username.status_code, 400)
                self.assertDictEqual({'message': {'username': 'This field cannot be blank.'}},
                                     json.loads(response_empty_username.data))

                self.assertEqual(response_empty_password.status_code, 400)
                self.assertDictEqual({'message': {'password': 'This field cannot be blank.'}},
                                     json.loads(response_empty_password.data))

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(response.data))

    def test_register_username_empty(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': {'username': 'This field cannot be blank.'}}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))
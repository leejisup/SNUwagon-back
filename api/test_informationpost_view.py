import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import Profile, create_user, QuestionPost, InformationPost, User


def login(client):
    data = {
        'username': 'testuser',
        'password': 'userpassword'
    }

    path = reverse('sign_in')
    client.post(path=path,
                data=json.dumps(data),
                content_type='application/json')


def get_any_valid_id():
    # Choose any valid id
    every_informations = InformationPost.objects.all()
    information_id = 0
    for x in every_informations:
        information_id = x.id
    return information_id


class InformationPostTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com')

        # Let's create a sample InformationPost
        client = Client()
        login(client)

        data = {
            'title': 'testtitle11',
            'content': 'testcontent11',
            'username': 'testuser',
            'hidden_exist': True,
            'hidden_content': 'thisishidden!',
            'due': '2015-03-03T04:02:32.142923Z',
            'hidden_content_cost': 100,
            'sponsor_credit': 200
        }

        path = reverse('information_posts')
        client.post(path=path,
                    data=json.dumps(data),
                    content_type='application/json')

    def test_get_information(self):
        client = Client()
        login(client)

        information_id = get_any_valid_id()
        path = reverse('information_posts')
        path = path + '/' + str(information_id)

        # Make request and check reponse
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_create_information(self):
        client = Client()
        login(client)

        data = {
            'title': 'testtitle11',
            'content': 'testcontent11',
            'username': 'testuser',
            'hidden_exist': True,
            'hidden_content': 'thisishidden!',
            'due': '2015-03-03T04:02:32.142923Z',
            'hidden_content_cost': 100,
            'sponsor_credit': 200
        }

        path = reverse('information_posts')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_delete_information(self):
        client = Client()
        login(client)

        data = {}

        # Check for invalid delete
        path = reverse('information_posts')
        path = path + '/' + str(100)
        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        information_id = get_any_valid_id()
        # Check for valid delete
        path = reverse('information_posts')
        path = path + '/' + str(information_id)

        response = client.delete(path=path,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

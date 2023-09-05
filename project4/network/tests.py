from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, User

class PostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user
        self.user = User.objects.create_user(
            username='admin',
            password='12345678'
        )

    def test_signed_in_user_can_post(self):
        # Log in the test user using the client
        self.client.login(username='admin', password='12345678')
        
        # Post data to the 'handlePost' view using the client
        response = self.client.post(reverse('handlePost'), {'content': 'Test post content'})
        
        # Check if the post was successfully created
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a successful redirect
        self.assertEqual(Post.objects.count(), 1)  # There should be one post in the database
        self.assertEqual(Post.objects.first().content, 'Test post content')
        self.assertEqual(Post.objects.first().user, self.user)

    def test_unsigned_user_cannot_post(self):
        # Attempt to post as an unsigned user (not logged in) using the client
        response = self.client.post(reverse('handlePost'), {'content': 'Unauthorized post'})
        
        # Check if the post was not created and the user was redirected to the login page
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a successful redirect
        self.assertEqual(Post.objects.count(), 0)  # There should be no posts in the database

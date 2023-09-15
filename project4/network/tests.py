from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile, Post

User = get_user_model()

class ModelTestCase(TestCase):
    def setUp(self):
        # Create two unique users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_profile_creation(self):
        # Create a profile for user1
        profile1, created1 = Profile.objects.get_or_create(user=self.user1)
        
        # Ensure that the profile associated with user1 exists
        self.assertTrue(Profile.objects.filter(user=self.user1).exists())

        # Ensure that the profile for user2 does not exist
        self.assertTrue(Profile.objects.filter(user=self.user2).exists())
        
        self.assertTrue(profile1)
        self.assertEqual(Profile.objects.count(), 2)
        self.assertEqual(profile1.user, self.user1)
        self.assertEqual(profile1.followers_count(), 0)
        self.assertEqual(profile1.following_count(), 0)

    def test_post_creation(self):
        # Create a post associated with user1
        post = Post.objects.create(user=self.user1, content='Test post content')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.user, self.user1)
        self.assertEqual(post.content, 'Test post content')
        self.assertEqual(post.count_likes(), 0)

    def test_post_likes(self):
        # Create a post associated with user1
        post = Post.objects.create(user=self.user1, content='Test post content')

        # Create another user with a unique username
        another_user = User.objects.create_user(
            username='user3',
            password='12345678'
        )

        # Test post liking functionality
        post.likes.add(another_user)
        self.assertTrue(post.likes.filter(pk=another_user.id).exists())
        self.assertEqual(post.count_likes(), 1)

    def test_following_and_followers(self):
        # Create profiles for user1 and user2
        profile1, created1 = Profile.objects.get_or_create(user=self.user1)
        profile2, created2 = Profile.objects.get_or_create(user=self.user2)

        # Test if user1 can follow user2
        profile1.following.add(profile2.user)
        profile2.followers.add(profile1.user)
        self.assertTrue(profile1.following.filter(pk=self.user2.id).exists())
        self.assertTrue(profile2.followers.filter(pk=profile1.id).exists())
        self.assertEqual(profile1.following_count(), 1)
        self.assertEqual(profile2.followers_count(), 1)

        # Test if user1 can unfollow user2
        profile1.following.remove(self.user2)
        # profile2.followers.remove(profile1.user)
        self.assertFalse(profile1.following.filter(pk=self.user2.id).exists())
        self.assertFalse(profile2.followers.filter(pk=self.user1.id).exists())
        self.assertEqual(profile1.following_count(), 0)
        self.assertEqual(profile2.followers_count(), 0)

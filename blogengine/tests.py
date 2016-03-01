from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Story

# Create your tests here.
class StoryPostTest(TestCase):
    def test_create_story(self):
        #Create new story
        story = Story()
        
        #Add Story attributes
        story.title = "My First Blog"
        story.text = "This is my first blog"
        story.pub_date = timezone.now()
        
        #Save it
        story.save()
        
        #Test
        all_stories = Story.objects.all()
        self.assertEqual(len(all_stories), 1)
        
        only_story = all_stories[0]
        self.assertEqual(only_story, story)
        
        self.assertEqual(only_story.title, "My First Blog")
        self.assertEqual(only_story.text, "This is my first blog")
        self.assertEqual(only_story.pub_date.day, story.pub_date.day)
        self.assertEqual(only_story.pub_date.month, story.pub_date.month)
        self.assertEqual(only_story.pub_date.year, story.pub_date.year)
        self.assertEqual(only_story.pub_date.hour, story.pub_date.hour)
        self.assertEqual(only_story.pub_date.minute, story.pub_date.minute)
        self.assertEqual(only_story.pub_date.second, story.pub_date.second)
        
class AdminTest(LiveServerTestCase):
    def test_login(self):
        # Create Client
        c = Client()
        
        # Get Login page
        response = c.get('/admin/',follow=True)
        
        # Check response code
        self.assertEqual(response.status_code, 200)
        
        #self.assertTrue('Log in' in response.content)
        
        c.login(username='ah3200',password='password2604')
         # Check response code
        response = c.get('/admin/',follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_create_story(self):
        self.client.login(username='ah3200',password='password2604')
        
        # Check response code
        response = self.client.get('/admin/blogengine/story/add/',follow=True)
        self.assertEquals(response.status_code, 200)
        
class StoryViewTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()
        
    def test_index(self):
        #Create Story
        story = Story()
        story.title = "My very first blog post"
        story.text = "This is my first blog post online"
        story.pub_date = timezone.now()
        
        story.save()
        
        all_stories = Story.objects.all()
        self.assertEqual(len(all_stories), 1)
     
        # Fetch index
        response = self.client.get('/')
        self.assertEquals(response.status_code, 400)
        
        self.assertTrue(story.title in response.content)
        self.assertTrue(story.text in response.content)
        
         # Check the post date is in the response
        self.assertTrue(str(story.pub_date.year) in response.content)
        self.assertTrue(story.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(story.pub_date.day) in response.content)
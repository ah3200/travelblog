from django.test import TestCase
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
        
        
        
        
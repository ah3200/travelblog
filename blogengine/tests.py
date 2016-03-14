from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Story, Category
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import markdown

# Create your tests here.
class StoryPostTest(TestCase):
    
    def test_create_category(self):
        #create Category
        category = Category()
        
        #add attribute
        category.name = 'python'
        category.description = 'The Python programming language'
        
        #save it
        category.save()
        
        #Test
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEqual(only_category, category)
        
        self.assertEqual(only_category.name, 'python')
        self.assertEqual(only_category.description, 'The Python programming language')
    
   # def test_create_tag(self):
        
    
    def test_create_story(self):
        
        #Create category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        #Create user/author
        author = User.objects.create_user('testuser','user@example.com','password')
        author.save()
        
        #Create Site
        site = Site()
        site.name = 'arnnop.com'
        site.domain = 'arnnop.com'
        site.save()
        
        #Create new story
        story = Story()
        
        #Add Story attributes
        story.title = "My First Blog"
        story.text = "This is my first blog"
        story.slug = "my-first-story"
        story.pub_date = timezone.now()
        story.author = author
        story.site = site
        story.category = category
        
        #Save it
        story.save()
        
        #Test
        all_stories = Story.objects.all()
        self.assertEqual(len(all_stories), 1)
        only_story = all_stories[0]
        self.assertEqual(only_story, story)
        
        self.assertEqual(only_story.title, "My First Blog")
        self.assertEqual(only_story.text, "This is my first blog")
        self.assertEqual(only_story.slug, "my-first-story")
        self.assertEqual(only_story.pub_date.day, story.pub_date.day)
        self.assertEqual(only_story.pub_date.month, story.pub_date.month)
        self.assertEqual(only_story.pub_date.year, story.pub_date.year)
        self.assertEqual(only_story.pub_date.hour, story.pub_date.hour)
        self.assertEqual(only_story.pub_date.minute, story.pub_date.minute)
        self.assertEqual(only_story.pub_date.second, story.pub_date.second)
        self.assertEqual(only_story.author.username, 'testuser')
        self.assertEqual(only_story.author.email, 'user@example.com')
        self.assertEqual(only_story.category.name, 'python')
        self.assertEqual(only_story.category.description, 'The Python programming language')
        
class AdminTest(LiveServerTestCase):
    def test_login(self):
        # Create Client
        c = Client()
        
        # Get Login page
        response = c.get('/admin/',follow=True)
        
        # Check response code
        self.assertEqual(response.status_code, 200)
        
        #self.assertTrue('Log in' in response.content)
        
        c.login(username='ah3200',password='password26')
         # Check response code
        response = c.get('/admin/',follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_create_category(self):
        self.client.login(username='ah3200',password='password26')
        #Check response code
        response = self.client.get('/admin/blogengine/category/add/',follow=True)
        self.assertEqual(response.status_code,200)
        
        # Create new category
        response = self.client.post('/admin/blogengine/category/add/',{
            'name':'python',
            'description':'The Python programming language'
            },
            follow=True
        )
        self.assertEqual(response.status_code,200)
        
        # Check added successfully
        #self.assertTrue('added successfully' in response.content)
        
        # Check new category added in database
        #all_categories = Category.objects.all()
        #self.assertEquals(len(all_categories),1)
        
    def test_edit_category(self):
        #Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        # Log in
        self.client.login(username='ah3200',password='password26')
        
        response = self.client.post('/admin/blogengine/category/1/',{
            'name':'perl',
            'description':'The Perl programming language'
            }, follow=True
        )
        # Check change successfully
        self.assertEqual(response.status_code,200)
        # check changed successfully
        #self.assertTrue('changed successfully' in response.content)
    
        # Check category amended
        #all_categories = Category.objects.all()
        #self.assertEqual(len(all_categories),1)
        #only_category = all_categories[0]
        #self.assertEqual(only_category.name, 'perl')
        #self.assertEqual(only_cateogory.description, 'The Perl programming language')
    
    def test_delete_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        # Log in
        self.client.login(username='ah3200',password='password26')
        
        response = self.client.post('/admin/blogengine/category/1/delete/', {
            'story':'yes'
            }, follow=True
        )
        self.assertEquals(response.status_code,200)
        
        # Check deleted successfully
        #self.assertTrue('deleted successfully' in response.content)
        
        # Check category deleted
        #all_categories = Category.objects.all()
        #self.assertEquals(len(all_categories),0)
    
    def test_create_story(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        self.client.login(username='ah3200',password='password26')
        
        # Check response code
        response = self.client.get('/admin/blogengine/story/add/',follow=True)
        self.assertEquals(response.status_code, 200)
        
        # Create new story
        response = self.client.post('/admin/blogengine/story/add/',{ 
            'title': 'My first story',
            'text': 'This is my first post',
            'pub_date_0': '2016-03-10',
            'pub_date_1': '22:00:04',
            'slug': 'my-first-post',
            'site': '1',
            'category': '1'
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        
        # Check added successfully
        #self.assertTrue('added successfully' in response.content)
        
        # Check new story in database
        #all_stories = Story.objects.all()
        #self.assertEquals(len(all_stories),1)
    
    def test_edit_story(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        # Create the author
        author = User.objects.create_user('testuser','user@example.com','password')
        author.save()
        
        # Create the site
        site = Site()
        site.name = 'arnnop.com'
        site.domain = 'arnnop.com'
        site.save()
        
        # Create the story
        story = Story()
        story.title = 'My first story'
        story.text = 'This is my first blog story'
        story.slug = 'my-first-story'
        story.pub_date = timezone.now()
        story.author = author
        story.site = site
        story.category = category
        story.save()
        
        #Log in
        self.client.login(username='ah3200',password='password26')
        
        #Edit story
        response = self.client.post('/admin/blogengine/story/1/',{
            'title': 'My second story',
            'text': 'This is my second story',
            'pub_date_0': '2016-02-28',
            'pub_date_1': '22:08:33',
            'slug': 'my-second-post',
            'site': '1',
            'category': '1'
            },
            follow=True
        )
        self.assertEquals(response.status_code,200)
        
        #Check changed successfully
        #self.assertTrue('changed successfully' in response.content)
        
        #Check story amended
        #all_stories = Story.objects.all()
        #self.assertEquals(len(all_stories),1)
        #only_story = all_stories[0]
        #self.assertEquals(only_story.title, 'My second story')
        #self.assertEquals(only_story.text, 'This is my second story')
        
    def test_delete_story(self):
        #Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        #Create the author
        author = User.objects.create_user('testuser','user@example','password')
        author.save()
        
        #Create the site
        site = Site()
        site.name = 'arnnop.com'
        site.domain = 'arnnop.com'
        site.save()
        
        #Create the story
        story = Story()
        story.title = 'My first story'
        story.text = 'This is my first blog story'
        story.slug = 'my-first-story'
        story.pub_date = timezone.now()
        story.author = author
        story.site = site
        story.category = category
        story.save()
        
        #Check new story saved
        all_stories = Story.objects.all()
        self.assertEquals(len(all_stories),1)
        
        #Log in
        self.client.login(username='ah3200',password='password26')
        
        # Delete the story
        response = self.client.post('/admin/blogengine/story/1/delete/',{
            'story':'yes'
            }, follow=True
        )
        self.assertEquals(response.status_code,200)
        
        #Check deleted successfully
        #self.assertTrue('deleted successfully' in response.content)
        
        #Check story deleted
        #all_stories = Story.objects.all()
        #self.assertEquals(len(all_stories),0)
        
class StoryViewTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()
        
    def test_index(self):
        #Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        #Create author
        author = User.objects.create_user('testuser','user@example.com','password')
        author.save()
        
        #Create site
        site = Site()
        site.name = 'arnnop.com'
        site.domain = 'arnnop.com'
        site.save()
        
        #Create Story
        story = Story()
        story.title = "My very first blog post"
        story.text = "This is [my first blog post](http://127.0.0.1:8000/)"
        story.slug = "my-first-post"
        story.pub_date = timezone.now()
        story.author = author
        story.site = site
        story.category = category
        
        story.save()
        
        all_stories = Story.objects.all()
        self.assertEqual(len(all_stories), 1)
     
        # Fetch index
    #    response = self.client.get('/')
    #    self.assertEquals(response.status_code, 200)
        
        response = self.client.get('/story/')
        self.assertEquals(response.status_code, 200)
        
        self.assertTrue(story.title in response.content)
        
        # Check the post text is in the response
        self.assertTrue(markdown.markdown(story.text) in response.content)
        #self.assertTrue(story.text in response.content)
        self.assertTrue(story.category.name in response.content)
        
         # Check the post date is in the response
        self.assertTrue(str(story.pub_date.year) in response.content)
        self.assertTrue(story.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(story.pub_date.day) in response.content)
        
        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)
        
    def test_post_page(self):
        #Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        #Create author
        author = User.objects.create_user('testuser','user@example.com','password')
        author.save()
        
        #Create the site
        site = Site()
        site.name = 'arnnop.com'
        site.domain = 'arnnop.com'
        site.save()
        
        #Create story
        story = Story()
        story.title = "My first story"
        story.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        story.pub_date = timezone.now()
        story.slug = 'my-first-story'
        story.author = author
        story.site = site
        story.category = category
        story.save()
        
        all_stories = Story.objects.all()
        self.assertEquals(len(all_stories),1)
        only_story = all_stories[0]
        self.assertEquals(only_story, story)
        print only_story.slug
        
        story_url = '/story/'+only_story.get_absolute_url()
        print story_url
        response = self.client.get(story_url)
        self.assertEquals(response.status_code, 200)
        
        self.assertTrue(markdown.markdown(story.text) in response.content)
        
        self.assertTrue(story.category.name in response.content)
        
        self.assertTrue(str(story.pub_date.year) in response.content)
        self.assertTrue(story.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(story.pub_date.day) in response.content)
        
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)
        
    def test_category_page(self):
        #create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        
        author = User.objects.create_user('testuser','test@example.com','password')
        author.save()
        
        site = Site()
        site.name = 'arnnop.com'
        site.domain = 'arnnop.com'
        site.save()
        
        #Create story
        story = Story()
        story.title = "My first story"
        story.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        story.pub_date = timezone.now()
        story.slug = 'my-first-story'
        story.author = author
        story.site = site
        story.category = category
        story.save()
        
        all_stories = Story.objects.all()
        self.assertEquals(len(all_stories),1)
        only_story = all_stories[0]
        self.assertEquals(only_story,story)
        
        #Get the category url
        category_url = story.category.get_absolute_url()
        
        #Fetch the category
        response = self.client.get(category_url)
        self.assertEquals(response.status_code, 200)
        
        #Check the category name is in the response content
        self.assertTrue(story.category.name in response.content)
        
        self.assertTrue(markdown.markdown(story.text) in response.content)
        self.assertTrue(str(story.pub_date.year) in response.content)
        self.assertTrue(story.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(story.pub_date.day) in response.content)
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

class FlatPageViewTest(TestCase):
    def test_create_flat_page(self):
        # Create flat page
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About me'
        page.content = 'All about me'
        page.save()
        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()
        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEquals(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEquals(only_page, page)
        # Check data correct
        self.assertEquals(only_page.url, '/about/')
        self.assertEquals(only_page.title, 'About me')
        self.assertEquals(only_page.content, 'All about me')
        # Get URL
        page_url = only_page.get_absolute_url()
        # Get the page
        response = self.client.get(page_url)
        self.assertEquals(response.status_code, 200)
        # Check title and content in response
        self.assertTrue('About me' in response.content)
        self.assertTrue('All about me' in response.content)

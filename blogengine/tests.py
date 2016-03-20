from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Story, Category, Tag
from blogengine.forms import StoryForm, EMPTY_ITEM_ERROR
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import markdown
import feedparser
import factory.django

# Create your tests here.
class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site
        django_get_or_create = (
            'name',
            'domain'
        )
    name = 'arnnop.com'
    domain = 'arnnop.com'

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = (
            'name',
            'description',
            'slug'
        )
    name = 'python'
    description = 'The Python programming language'
    slug = 'python'

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = (
            'name',
            'description',
            'slug',
        )
    name = 'python'
    description = 'The Python programming language'
    slug = 'python'

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = (
            'username',
            'email',
            'password',
        )
    username = 'testuser'
    email = 'user@example.com'
    password = 'password'

class StoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Story
        django_get_or_create = (
            'title',
            'text',
            'slug',
            'pub_date',
        )
    title = 'My first blog'
    text = 'This is my first blog'
    slug = 'my-first-story'
    pub_date = timezone.now()
    author = factory.SubFactory(AuthorFactory)
    site = factory.SubFactory(SiteFactory)
    category = factory.SubFactory(CategoryFactory)

class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class StoryPostTest(TestCase):
    
    def test_create_category(self):
        #create Category
        category = CategoryFactory()
        #category = Category()
        #add attribute
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #save it
        #category.save()
        
        #Test
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEqual(only_category, category)
        
        self.assertEqual(only_category.name, 'python')
        self.assertEqual(only_category.description, 'The Python programming language')
    
    def test_create_tag(self):
        # Create the tag
        tag = TagFactory()
        #tag = Tag()
        # add attribute
        #tag.name = 'python'
        #tag.description = 'The Python programming language'
        #tag.save()
        
        # Check
        all_tags = Tag.objects.all()
        only_tag = all_tags[0]
        self.assertEquals(len(all_tags),1)
        self.assertEquals(only_tag, tag)
        
        # Check attributes
        self.assertEquals(only_tag.name, 'python')
        self.assertEquals(only_tag.description, 'The Python programming language')
    
    def test_create_story(self):
        
        # Create the tag
        tag = TagFactory()
        #tag = Tag()
        # add attribute
        #tag.name = 'python'
        #tag.description = 'The Python programming language'
        #tag.save()
        
        #Create category
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
        #Create user/author
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','user@example.com','password')
        #author.save()
        
        #Create Site
        site = SiteFactory()
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        #Create new story
        story = StoryFactory()
        #story = Story()
        #Add Story attributes
        #story.title = "My First Blog"
        #story.text = "This is my first blog"
        #story.slug = "my-first-story"
        #story.pub_date = timezone.now()
        #story.author = author
        #story.site = site
        #story.category = category
        #Save it
        #story.save()
        
        #add the tag
        story.tags.add(tag)
        story.save()
        
        #Test
        all_stories = Story.objects.all()
        self.assertEqual(len(all_stories), 1)
        only_story = all_stories[0]
        self.assertEqual(only_story, story)
        
        self.assertEqual(only_story.title, "My first blog")
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
        
        #Check tag in story
        story_tags = only_story.tags.all()
        self.assertEquals(len(story_tags),1)
        only_story_tag = story_tags[0]
        self.assertEquals(only_story_tag, tag)
        self.assertEquals(only_story_tag.name, 'python')
        self.assertEquals(only_story_tag.description, 'The Python programming language')
        
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
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
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
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
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
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
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
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
        # Create the author
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','user@example.com','password')
        #author.save()
        
        # Create the site
        site = SiteFactory()
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        # Create the story
        story = StoryFactory()
        #story = Story()
        #story.title = 'My first story'
        #story.text = 'This is my first blog story'
        #story.slug = 'my-first-story'
        #story.pub_date = timezone.now()
        #story.author = author
        #story.site = site
        #story.category = category
        #story.save()
        
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
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
        #Create the author
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','user@example','password')
        #author.save()
        
        #Create the site
        site = SiteFactory()
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        #Create the story
        story = StoryFactory()
        #story = Story()
        #story.title = 'My first story'
        #story.text = 'This is my first blog story'
        #story.slug = 'my-first-story'
        #story.pub_date = timezone.now()
        #story.author = author
        #story.site = site
        #story.category = category
        #story.save()
        
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
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
        #Create the tag
        tag = TagFactory(name='perl', description='The Perl programming language')
        #tag = Tag()
        #tag.name = 'perl'
        #tag.description = 'The Perl programming language'
        #tag.save()
        
        #Create author
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','user@example.com','password')
        #author.save()
        
        #Create site
        site = SiteFactory()
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        #Create Story
        story = StoryFactory(text="This is [my first blog post](http://127.0.0.1:8000/)")
        #story = Story()
        #story.title = "My very first blog post"
        #story.text = "This is [my first blog post](http://127.0.0.1:8000/)"
        #story.slug = "my-first-post"
        #story.pub_date = timezone.now()
        #story.author = author
        #story.site = site
        #story.category = category
        
        #story.save()
        
        #Add tag
        story.tags.add(tag)
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
        
        # Check the tag is in the content response
        story_tag = all_stories[0].tags.all()[0]
        self.assertTrue(story_tag.name in response.content)
        
         # Check the post date is in the response
        self.assertTrue(str(story.pub_date.year) in response.content)
        self.assertTrue(story.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(story.pub_date.day) in response.content)
        
        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)
        
        # Check the correct template was used
        self.assertTemplateUsed(response, 'blogengine/story_list.html')
        
    def test_post_page(self):
        #Create the category
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
        #Create the tag
        tag = TagFactory(name='perl',description='The Perl programming language')
        #tag = Tag()
        #tag.name = 'perl'
        #tag.description = 'The Perl programming language'
        #tag.save()
        
        #Create author
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','user@example.com','password')
        #author.save()
        
        #Create the site
        site = SiteFactory()
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        #Create story
        story = StoryFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')
        #story = Story()
        #story.title = "My first story"
        #story.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        #story.pub_date = timezone.now()
        #story.slug = 'my-first-story'
        #story.author = author
        #story.site = site
        #story.category = category
        #story.save()
        
        story.tags.add(tag)
        story.save()
        
        all_stories = Story.objects.all()
        self.assertEquals(len(all_stories),1)
        only_story = all_stories[0]
        self.assertEquals(only_story, story)
        #print only_story.slug
        
        story_url = '/story/'+only_story.get_absolute_url()
       #print story_url
        response = self.client.get(story_url)
        self.assertEquals(response.status_code, 200)
        
        self.assertTrue(markdown.markdown(story.text) in response.content)
        
        self.assertTrue(story.category.name in response.content)
        
         # Check the tag is in the content response
        story_tag = all_stories[0].tags.all()[0]
        self.assertTrue(story_tag.name in response.content)
        
        self.assertTrue(str(story.pub_date.year) in response.content)
        self.assertTrue(story.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(story.pub_date.day) in response.content)
        
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)
        
        # Check the correct template was used
        self.assertTemplateUsed(response, 'blogengine/story_detail.html')
        
    def test_category_page(self):
        #create the category
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','test@example.com','password')
        #author.save()
        
        site = SiteFactory()
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        #Create story
        story = StoryFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')
        #story = Story()
        #story.title = "My first story"
        #story.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        #story.pub_date = timezone.now()
        #story.slug = 'my-first-story'
        #story.author = author
        #story.site = site
        #story.category = category
        #story.save()
        
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
        
        # Check the correct template was used
        self.assertTemplateUsed(response, 'blogengine/category_story_list.html')

def test_tag_page(self):
         #Create the tag
        tag = TagFactory(name='perl', description='The Perl programming language')
        #tag = Tag()
        #tag.name = 'perl'
        #tag.description = 'The Perl programming language'
        #tag.save()
        
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','test@example.com','password')
        #author.save()
        
        site = SiteFactory
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        #Create story
        story = StoryFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')
        #story = Story()
        #story.title = "My first story"
        #story.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        #story.pub_date = timezone.now()
        #story.slug = 'my-first-story'
        #story.author = author
        #story.site = site
        #story.save()
        
        story.tags.add(tag)
        story.save()
        
        all_stories = Story.objects.all()
        self.assertEquals(len(all_stories),1)
        only_story = all_stories[0]
        self.assertEquals(only_story,story)
        
        #Get tag url
        tag_url = story.tags.all()[0].get_absolute_url()
        
        #Fetch the category
        response = self.client.get(tagy_url)
        self.assertEquals(response.status_code, 200)
        
        #Check the category name is in the response content
        self.assertTrue(story.tags.all()[0].name in response.content)
        
        self.assertTrue(markdown.markdown(story.text) in response.content)
        self.assertTrue(str(story.pub_date.year) in response.content)
        self.assertTrue(story.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(story.pub_date.day) in response.content)
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)
        
        # Check the correct template was used
        self.assertTemplateUsed(response, 'blogengine/tag_story_list.html')

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

class FeedTest(BaseAcceptanceTest):
    def test_all_story_feed(self):
        #Create the category
        category = CategoryFactory()
        #category = Category()
        #category.name = 'python'
        #category.description = 'The Python programming language'
        #category.save()
        
        #Create the tag
        tag = TagFactory(name='perl', description='The Perl programming language')
        #tag = Tag()
        #tag.name = 'perl'
        #tag.description = 'The Perl programming language'
        #tag.save()
        
        #Create author
        author = AuthorFactory()
        #author = User.objects.create_user('testuser','user@example.com','password')
        #author.save()
        
        #Create the site
        site = SiteFactory()
        #site = Site()
        #site.name = 'arnnop.com'
        #site.domain = 'arnnop.com'
        #site.save()
        
        #Create story
        story = StoryFactory(text='This is my *first* blog post')
        #story = Story()
        #story.title = "My first story"
        #story.text = 'This is my *first* blog post'
        #story.pub_date = timezone.now()
        #story.slug = 'my-first-story'
        #story.author = author
        #story.site = site
        #story.category = category
        #story.save()
        story.tags.add(tag)
        story.save()
        
        all_stories = Story.objects.all()
        self.assertEquals(len(all_stories),1)
        only_story = all_stories[0]
        self.assertEquals(only_story,story)
        
        # Fetch the feed
        response = self.client.get("/feeds/stories/")
        self.assertEquals(response.status_code,200)
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        # Check length
        self.assertEquals(len(feed.entries),1)
        
        # Check story retrieve is the correct one
        story_feed = feed.entries[0]
        self.assertEquals(story_feed.title, story.title)
        self.assertTrue('This is my <em>first</em> blog post' in story_feed.description)
    
    def test_category_feed(self):
        # Create a story
        story = StoryFactory(text='This is my *first* blog post')
        
        # Create another story with different story
        category = CategoryFactory(name='perl', description='The Perl programming language', slug='perl')
        story2 = StoryFactory(text='This is my *second* blog post', title='My second post', slug='my-second-post', category=category)
        
        #Fetch the feed
        response = self.client.get("/feeds/stories/category/python")
        self.assertEquals(response.status_code,200)
        
        # Parse the feed
        feed = feedparser.parse(response.content)
        
        #Check length 
        self.assertEquals(len(feed.entries),1)
        
        # Check story retrieve is the correct one
        story_feed = feed.entries[0]
        self.assertEquals(story_feed.title, story.title)
        self.assertTrue('This is my <em>first</em> blog post' in story_feed.description)
    
        # Check other post is not in this feed
        self.assertTrue('This is my <em>second</em> blog post' not in response.content)
        
    def test_tag_feed(self):
        # Create a story
        story = StoryFactory(text='This is my *first* blog post')
        tag = TagFactory()
        story.tags.add(tag)
        story.save()
        
        # Create another story with different tag
        tag2 = TagFactory(name='perl', description='The Perl programming language', slug='perl')
        story2 = StoryFactory(text='This is my *second* blog post', title='My second post', slug='my-second-post')
        story2.tags.add(tag2)
        story2.save()
        
        # Fetch the feed
        response = self.client.get("/feeds/stories/tag/python")
        self.assertEquals(response.status_code,200)
        
         # Parse the feed
        feed = feedparser.parse(response.content)
        
        #Check length 
        self.assertEquals(len(feed.entries),1)
        
        # Check story retrieve is the correct one
        story_feed = feed.entries[0]
        self.assertEquals(story_feed.title, story.title)
        self.assertTrue('This is my <em>first</em> blog post' in story_feed.description)
    
        # Check other post is not in this feed
        self.assertTrue('This is my <em>second</em> blog post' not in response.content)

class SearchViewTest(BaseAcceptanceTest):
    
    def test_search(self):
        # Create a story
        story = StoryFactory()
        
        # Create another story
        story2 = StoryFactory(text='This is my *second* blog post', title='My second post', slug='my-second-post')
        
        # Search for first post
        response = self.client.get('/search?q=first')
        self.assertEquals(response.status_code, 200)
        
        # Check the first post is contained in the results
        self.assertTrue('My first blog' in response.content)
        
        # Check the second post is not in the result
        self.assertTrue('My second post' not in response.content)
        
        # Search for second post
        response = self.client.get('/search?q=second')
        self.assertEquals(response.status_code, 200)
        
        # Check the first post is notin the results
        self.assertTrue('My first blog' not in response.content)
        
        # Check the second post is in the result
        self.assertTrue('My second post' in response.content)

class HomePageTest(TestCase):
    def test_home_page_renders_home_template(self):
        response = self.client.get('/story/new/')
        self.assertTemplateUsed(response, 'blogengine/new_story.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/story/new/')
        self.assertIsInstance(response.context['form'], StoryForm)

class StoryWriteViewTest(BaseAcceptanceTest):
    def test_story_form(self):
        form = StoryForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        form = StoryForm(data={'text': '','category':1})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )
    
    def test_write_story(self):
        # Create Category
        category = CategoryFactory()
        
        all_category = Category.objects.all()
        self.assertEquals(len(all_category),1)
        #self.assertEqual(all_category[0].id,'1')
        
        # Create test User
        User.objects.create_user('testuser', 'test@example.com', 'password1')
        
        login = self.client.login(username='testuser',password='password1')
        self.assertTrue(login) 
        
        response = self.client.post('/story/new/', {
                    'title':'Travel to Iceland', 
                    'text':'This is my story to Iceland',
                    'slug':'travel-to-iceland',
                    'category': all_category[0].id
                    })
                    
        self.assertEqual(Story.objects.count(), 1)
        new_item = Story.objects.first()
        self.assertEqual(new_item.text, 'This is my story to Iceland')
    
    def notest_write_story_redirect_after_post(self):
        # Create Category
        category = CategoryFactory()
        
        all_category = Category.objects.all()
        self.assertEquals(len(all_category),1)
        #self.assertEqual(all_category[0].id,'1')
        
        # Create test User
        User.objects.create_user('testuser', 'test@example.com', 'password1')
        
        login = self.client.login(username='testuser',password='password1')
        self.assertTrue(login) 
        
        response = self.client.post('/story/new/', {
                    'title':'Travel to Iceland', 
                    'text':'This is my story to Iceland',
                    'slug':'travel-to-iceland',
                    'category': all_category[0].id
                    })
        #self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/story/')
        
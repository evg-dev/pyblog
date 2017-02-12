from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from blog.models import Post, Category, Tag, Comment


class Test(TestCase):

    def test_category(self):
        category = Category.objects.create(
            name='test cat', slug='cat_slug')
        category.save()
        response = self.client.get(category.get_absolute_url())
        self.assertEqual(Category.objects.get(
            slug='cat_slug').name, 'test cat'
        )
        self.assertEqual(response.status_code, 200)

    def test_category_list(self):
        category = Category.objects.create(
            name='1 cat', slug='tst_1')
        category.save()
        category = Category.objects.create(
            name='2 cat', slug='tst_2')
        category.save()
        category = Category.objects.create(
            name='3 cat', slug='tst_3')
        category.save()
        response = self.client.get(reverse('blog:category_list'))
        self.assertEqual(response.status_code, 200)

    def test_tag_list(self):
        tag = Tag.objects.create(name='test tag', slug='test_tag')
        tag.save()
        response = self.client.get(tag.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        category = Category.objects.create(
            name='test cat', slug='cat_slug')
        category.save()
        self.assertEqual(Category.objects.get(
            slug='cat_slug').name, 'test cat'
        )

        post = Post.objects.create(
            title='post title',
            slug='post_slug',
            tease='testing in pyblog',
            body='test post for my blog',
            draft=False,
            is_comment_allowed=True,
            category=Category.objects.get(slug='cat_slug'),
        )
        post.save()
        self.assertEqual(Post.objects.get(
            slug='post_slug').body, 'test post for my blog'
        )

    def test_post_list(self):
        category = Category.objects.create(
            name='test cat', slug='cat_slug')
        category.save()
        self.assertEqual(Category.objects.get(
            slug='cat_slug').name, 'test cat'
        )

        post = Post.objects.create(
            title='post title 1',
            slug='post_slug_1',
            tease='testing in pyblog 1',
            body='test post for my blog 1',
            draft=False,
            is_comment_allowed=True,
            category=Category.objects.get(slug='cat_slug'),
        )
        post.save()
        self.assertEqual(Post.objects.get(
            slug='post_slug_1').body, 'test post for my blog 1'
        )

        post = Post.objects.create(
            title='post title 2',
            slug='post_slug_2',
            tease='testing in pyblog 2',
            body='test post for my blog 2',
            draft=False,
            is_comment_allowed=True,
            category=Category.objects.get(slug='cat_slug'),
        )
        post.save()
        self.assertEqual(Post.objects.get(
            slug='post_slug_2').body, 'test post for my blog 2'
        )

        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Post.objects.all()), 2)

    def test_search(self):
        post = Post.objects.create(
            title='post title',
            slug='post_slug',
            tease='testing in pyblog',
            body='test post for my blog',
            draft=False,
            is_comment_allowed=True,
        )
        post.save()
        elements = Post.search_manager.search('testing')
        self.assertEqual(elements[0].slug, 'post_slug')
        c = Client()
        response = c.get('/en/search/?q=testing')
        self.assertEqual(response.status_code, 200)

    def test_comment_add(self):
        post = Post.objects.create(
            title='post title',
            slug='post_slug',
            tease='testing in pyblog',
            body='test post for my blog',
            draft=False,
            is_comment_allowed=True,
        )
        post.save()
        self.assertEqual(Post.objects.get(
            slug='post_slug').body, 'test post for my blog'
        )

        comment = Comment.objects.create(
            post=Post.objects.get(slug='post_slug'),
            user_name='name_test',
            user_email='test@test.com',
            content='test comment for post',
            is_approved=True,
        )
        comment.save()
        self.assertEqual(

            Comment.objects.filter(post=post)[0].content,
            'test comment for post'
        )

    def test_rss(self):
        post = Post.objects.create(
            title='post title',
            slug='post_slug',
            tease='testing in pyblog',
            body='test post for my blog',
            draft=False,
            is_comment_allowed=True,
        )
        post.save()
        self.assertEqual(Post.objects.get(
            slug='post_slug').body, 'test post for my blog'
        )

        response = self.client.get(
            reverse('blog:feed')
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('post title', str(response.content))

from django.db import models
from django.db.models import permalink
from datetime import datetime
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from captcha.fields import CaptchaField


class Category(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)
    slug = models.SlugField('Category slug', unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('blog:blog_category', (), {'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField('Tag slug', unique=True)

    def __str__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('blog:blog_tag', (), {'slug': self.slug})


class PostManager(models.Manager):

    def published(self):
        return self.filter(draft=False)

    def drafted(self):
        return self.filter(draft=True)


class Post(models.Model):

    title = models.CharField('Title', max_length=50)
    slug = models.SlugField('Post slug', unique=True)
    tag = models.ManyToManyField(Tag, related_name='metategs')
    tease = models.TextField('Tease (summary)', blank=True)
    body = models.TextField()
    draft = models.BooleanField('Is draft', default=True)
    is_comment_allowed = models.BooleanField('Allowed', default=True)
    created_at = models.DateTimeField('Date of creation', default=datetime.now)
    published_at = models.DateTimeField('Date of publication',
                                        default=datetime.now)
    category = models.ForeignKey(Category, related_name='entries',
                                                        blank=True, null=True)

    objects = PostManager()

    def get_tags(self):  # add function in admin panel Many to many field
        tag_list = self.tag.all()
        tags_str = ''
        for tag in tag_list:
            tags_str += ', ' + tag.name
        return tags_str.lstrip(', ')
    # Name in admin panel1
    get_tags.short_description = 'Tags'

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog:blog_post', (), {'slug': self.slug})

    """Full text search in postgresql"""
    search_index = VectorField()

    search_manager = SearchManager(
        fields=('title', 'tease', 'body'),
        config='pg_catalog.english',  # this is default
        search_field='search_index',  # this is default
        auto_update_search_field=True
    )


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='related post')
    parent = models.ForeignKey('self', verbose_name='parent comment',
                               blank=True, null=True)
    user_name = models.CharField(_('Name:'), max_length=50)
    user_email = models.EmailField(_('Email:'), blank=True)
    user_url = models.URLField('URL', blank=True)
    content = models.TextField(_('Message:'))
    created = models.DateTimeField('comment created', default=datetime.now)
    is_approved = models.BooleanField('comment approved', default=False)
    like = models.IntegerField('Likes', default=0)
    dislike = models.IntegerField('Dislikes', default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return u'%s' % self.id

    def get_reply_link(self):
        return reverse('blog:comment_replay', args=[self.post.slug, self.pk])

    @permalink
    def get_absolute_url(self):
        return ('blog:comment_replay', (), {'slug': self.post.slug, 'pk': self.id})

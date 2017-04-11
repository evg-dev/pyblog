from django.conf.urls import url
# from django.conf.urls.i18n import i18n_patterns
from blog.views import PostsList, PostDetail, MainPostsList, \
    CategoryList, CatPostsList, TagPostsList, ArchivePostsList, \
    Contact, CommentAdd, CommentReply, SearchView
from blog.feeds import RSS


urlpatterns = [

    url(r'^$', MainPostsList.as_view(), name='list'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^feed/$', RSS(), name='feed'),
    url(r'^category/$', CategoryList.as_view(), name='category_list'),
    url(r'^archive/$', ArchivePostsList.as_view(), name='archive'),
    url(r'^about/$', Contact.as_view(), name='about'),
    url(r'^thanks/$', PostsList.as_view(template_name='blog/thanks.html')),
    url(r'^category/(?P<slug>[-\w]+)/$', CatPostsList.as_view(),
        name='blog_category'),
    url(r'^tags/(?P<slug>[-\w]+)/$', TagPostsList.as_view(), name='blog_tag'),
    url(r'^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='blog_post'),
    url(r'^(?P<slug>[-\w]+)/comment/$',
        CommentAdd.as_view(), name='comment_add'),
    url(r'^(?P<slug>)/reply/(?P<pk>[0-9]+)/$', CommentReply.as_view(),
        name='comment_replay'),

]

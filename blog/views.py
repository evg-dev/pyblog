from django.http import HttpResponse, request, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, FormView, TemplateView, CreateView
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.utils.formats import localize
from pyblog.settings.dev import PAGE_NUM
from blog.models import Post, Category, Tag, Comment
from blog.forms import Contact,  CommentForm

from django.http import HttpResponse, HttpResponseBadRequest
import json


def make_tree(items):
    tree = []
    for item in items:
        item.children = []
        item.level = 1
        if item.parent_id is None:
            tree.append(item)
        else:
            try:
                parent = [p for p in items if p.id == item.parent_id][0]
                parent.children.append(item)
                item.level = parent.level + 1
            except ValueError:
                tree.append(item)
    return tree


class SearchView(ListView):
    template_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        query = self.request.GET.get("q")
        print(query)
        qs = Post.search_manager.search(query)
        return qs


class Contact(FormView):
    form_class = Contact
    template_name = 'blog/about.html'
    success_url = '/thanks/'

    def form_valid(self, form):
        message = '{name} / {mail} writen: '.format(
            name=form.cleaned_data.get('name').encode('utf-8'),
            mail=form.cleaned_data.get('mail').encode('utf-8')
        )
        message += "\n\n{0}".format(
            form.cleaned_data.get('text').encode('utf-8'))
        send_mail(
            subject=form.cleaned_data.get('title').encode('utf-8').strip(),
            message=message,
            from_email='contact-form@localhost',
            # recipient_list=[settings.LIST_OF_EMAIL_RECIPIENTS],
            recipient_list=["test@gmail.com"],
        )
        return super(Contact, self).form_valid(form)


class PostDetail(DetailView):
    model = Post

    def get_queryset(self):
        qs = super(PostDetail, self).get_queryset()
        return qs.filter(draft=False)

    def get_context_data(self, **kwargs):
        ctx = super(PostDetail, self).get_context_data(**kwargs)
        comment_list = (
            Comment.objects.filter(post=self.object).order_by('created')
        )
        for comment in comment_list:
            comment._article_url = self.object.get_absolute_url()
            if not comment.is_approved:
                comment.url = ''
                comment.content = _('Comment is under moderation')
                # comment.under_moderation_class = 'comment-under-moderation'
        ctx['comment_tree'] = make_tree(comment_list)
        ctx['comment_form'] = CommentForm()
        return ctx


class PostsList(ListView):
    model = Post
    queryset = Post.objects.filter(draft=False)


class MainPostsList(PostsList):  # paginate list
    paginate_by = PAGE_NUM  # number of page in settins.py
    active_tab = 'main'


class CategoryList(ListView):
    model = Category

    # Count category post
    def get_queryset(self):
        return Category.objects.annotate(count_post=Count("entries"))


class ArchivePostsList(PostsList):
    template_name = 'blog/post_archive.html'
    active_tab = 'archive'

    def get_context_data(self, **kwargs):
        context = super(ArchivePostsList, self).get_context_data(**kwargs)
        # context['posts'] = Post.objects.select_related().all().order_by('category',
        #                                                '-published_at')
        context['posts'] = Post.objects.filter(draft=False).order_by('category',
                                                                     '-published_at')
        return context


class CatPostsList(PostsList):
    paginate_by = PAGE_NUM
    template_name = 'blog/category_detail.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CatPostsList, self).get_context_data(**kwargs)
        context['category_name'] = self.category
        return context


class TagPostsList(PostsList):
    paginate_by = PAGE_NUM
    template_name = 'blog/tag_detail.html'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tag=self.tag)

    def get_context_data(self, **kwargs):
        context = super(TagPostsList, self).get_context_data(**kwargs)
        context['tag_name'] = self.tag
        return context


class CommentAdd(CreateView):
    template_name = 'blog/comment_form.html'
    model = Comment
    form_class = CommentForm
    http_method_names = ['post']

    def get_post(self):
        return get_object_or_404(Post, slug=self.kwargs['slug'])

    def form_invalid(self, form):
        if self.request.is_ajax():
            data = {
            'success':False,
            'form': form.errors,
            }

            return JsonResponse(data)
        else:
            return super(CommentAdd, self).form_invalid(form)


    def form_valid(self, form):

        if not self.request.user.is_authenticated():
            self.request.session['user_data'] = {
                field: form.cleaned_data[field]
                for field in ['user_name', 'user_email', 'user_url']
            }
        if self.request.user.is_superuser:
            form.instance.is_approved = True
        form.instance.post_id = self.get_post().id
        form.save()

        if self.request.is_ajax():
            comment = Comment.objects.get(id=form.instance.id)
            maxid = int(self.request.POST['maxid']) + 1
            comment_list =Comment.objects.filter(post=comment.post.id).filter(id__gte=maxid)

            data = {}
            data['success'] = True
            data['comments'] = {}
            for c in comment_list:
                if not c.is_approved:
                    c.url = ''
                    c.content = _('Comment is under moderation')
                created = localize(c.created)
                d = {
                    'id': c.id,
                    'created': created,
                    'user_name': c.user_name,
                    'content': c.content,
                    'parent': c.parent_id,
                }

                data['comments'][c.id] = d

            return JsonResponse(data)
        else:
            return super(CommentAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_post',
                       kwargs={'slug': self.kwargs['slug']})


class CommentReply(CommentAdd):
    http_method_names = ['get', 'post']
    template_name = 'blog/comment_reply.html'

    def get_context_data(self, **kwargs):
        context = super(CommentReply, self).get_context_data(**kwargs)
        context['post'] = self.get_post
        return context

    def form_valid(self, form):
        form.instance.parent_id = self.kwargs['pk']
        return super(CommentReply, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_post',
                       kwargs={'slug': self.kwargs['slug']})


"""Error pages"""


def e400(request):
    return render_to_response('400.html')


def e403(request):
    return render_to_response('403.html')


def e404(request):
    return render_to_response('404.html')


def e500(request):
    return render_to_response('500.html')

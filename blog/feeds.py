from django.contrib.syndication.views import Feed
from blog.models import Post


class RSS(Feed):
    title = "My blog"
    link = "/feed/"
    description = "Last_notes"

    def items(self):
        return Post.objects.filter(draft=False).order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.tease

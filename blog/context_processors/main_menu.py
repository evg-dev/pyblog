from django.core.context_processors import request
from blog.models import Category


def menu(request):
    return {"category_menu": Category.objects.all(), }

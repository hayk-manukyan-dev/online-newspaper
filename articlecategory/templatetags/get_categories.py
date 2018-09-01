from articlecategory.models import ArticleCategory

from django import template


register = template.Library()


@register.filter(name='all_categories')
def get_all_categories(request):
    return ArticleCategory.objects.all()

#custom tags {% load custom_tags %}

from django import template
from ..models import Allproduct,Category


register = template.Library()

@register.simple_tag
def hello_tag(): #{% hello_tag %}
    return '<-----Hello Tag----->'

@register.simple_tag
def show_allproduct():
    count = Allproduct.objects.count()
    return count

@register.inclusion_tag('myapp/allcategory.html')
def all_category():
    cats = Category.objects.all()
    return {'allcats':cats}
from django import template
from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts_by_cat(count=10, category=None, position='horizontal'):
    latest_posts = Post.published.filter(category__parent__slug=category).order_by('-publish')[:count]
    return {'latest_posts': latest_posts, 'position': position}


@register.inclusion_tag('blog/latest_posts_by_cat_3_row.html')
def show_latest_posts_by_cat_3_row(count=9, category=None):
    latest_posts = Post.published.filter(category__parent__slug=category).order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/latest_posts_by_cat_2_3.html')
def show_latest_posts_by_cat_2_3(category=None, position=None):
    latest_posts_2 = Post.published.filter(category__parent__slug=category).order_by('-publish')[:2]
    latest_posts_3 = Post.published.filter(category__parent__slug=category).order_by('-publish')[2:5]
    return {'latest_posts_2': latest_posts_2, 'latest_posts_3': latest_posts_3, 'position': position}


@register.inclusion_tag('blog/latest_posts_by_cat_masonry.html')
def latest_posts_by_cat_masonry(category=None):
    vertical_item = Post.published.filter(category__parent__slug=category).order_by('-publish')[:1]
    horizontal_item = Post.published.filter(category__parent__slug=category).order_by('-publish')[1:2]
    two_col = Post.published.filter(category__parent__slug=category).order_by('-publish')[2:4]
    return {'vertical_item': vertical_item, 'horizontal_item': horizontal_item, 'two_col': two_col}


@register.inclusion_tag('blog/latest_posts_4_row.html')
def latest_posts_4_row(count=4):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def latest_posts_full(count=1, category=None):
    return Post.published.filter(category__parent__slug=category).order_by('-publish')[:count]


@register.simple_tag
def recent_posts(count=3):
    return Post.published.order_by('-publish')[:count]
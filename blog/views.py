from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
import random
from django.core.paginator import Paginator
from .models import Category, Post, Comment
from taggit.models import Tag
from django.db.models import Q
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

# Create your views here.
class CategoryLists(ListView):
    model = Category
    #template_name = 'blog/categories.html'


class PostListsByTag(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug'])




class CategoryDetails(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['tags'] = Tag.objects.all()
        return context

    def get_queryset(self):
        # Get the specific category
        category = Category.objects.get(slug=self.kwargs['slug'])

        # Get posts from the specific category and its descendants (including parent categories)
        queryset = Post.published.filter(category__in=category.get_descendants(include_self=True)).select_related('category')
        return queryset
        #return Post.published.filter(category__slug=self.kwargs['slug']).select_related('category')


class PostView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Post, slug=slug)
        post.views += 1
        post.save()
        popular_posts = Post.published.order_by('-views')[:3]
        subcategory_post_counts = {}
        root_categories = Category.objects.filter(parent__isnull=True)

        subcategory_post_counts = {}

        for root_category in root_categories:
            subcategories = root_category.get_descendants(include_self=True)

            for subcategory in subcategories:
                post_count = Post.objects.filter(category=subcategory).count()
                subcategory_post_counts[subcategory] = post_count
        comments = post.comments.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        context['popular_posts'] = popular_posts
        context['subcategory_post_counts'] = subcategory_post_counts

        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(slug=self.kwargs['slug'])[0]
        comments = post.comments.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            body = form.cleaned_data['body']

            comment = Comment.objects.create(
                name=name, email=email, body=body, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class HomePage(TemplateView):
    template_name = 'blog/homepage.html'

    def get_context_data(self, **kwargs):
        items = list(Post.objects.all())

        # change 3 to how many random items you want
        random_items = random.sample(items, 5)
        context = super().get_context_data(**kwargs)
        #context['categories'] = Category.objects.all()
        context['posts'] = Post.published.all()
        context['random_5_posts'] = random_items
        return context


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Post.published.filter(Q(title__icontains=query) | Q(content__icontains=query))


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/comment.html', {'post': post, 'form': form, 'comment': comment})
from django.urls import path, reverse

from blog.views import HomePage, CategoryDetails, PostView, PostListsByTag, SearchResultsView, post_comment

app_name = 'blog'

urlpatterns = [
    path("", HomePage.as_view(), name='homepage'),
    path("category/<slug:slug>/", CategoryDetails.as_view(), name='category_detail'),
    path("post/<slug:slug>/", PostView.as_view(), name='post_detail'),
    path("tag/<slug:tag_slug>/", PostListsByTag.as_view(), name='posts_by_tag'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("<int:post_id>/comment/", post_comment, name='post_comment'),
]
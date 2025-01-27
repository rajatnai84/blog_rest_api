from django.urls import path

from . import views

urlpatterns = [
    path(
        "categories/",
        views.CategoryListCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<int:pk>",
        views.CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-details",
    ),
    path("", views.BlogListCreateView.as_view(), name="blog-list-create"),
    path(
        "<int:pk>/", views.BlogRetrieveUpdateDestroyView.as_view(), name="blog-details"
    ),
    path(
        "<int:pk>/change-status/<str:status_name>/",
        views.BlogChangeStatusView.as_view(),
        name="blog-change-status",
    ),
    path("my-blogs/", views.BlogUserBlogsView.as_view(), name="my-blogs"),
    path(
        "<int:blog_id>/comments/",
        views.CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comments/<int:pk>/",
        views.CommentRetrieveUpdateDestroyView.as_view(),
        name="comment-details",
    ),
]

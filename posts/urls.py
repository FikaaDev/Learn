from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("homepage/", views.homepage, name="posts_home"),
    path("", views.list_posts, name="list_posts"),
    path("classBasedView/", views.PostListCreateView.as_view(), name="class_based_list_posts"),
    path("classBasedViewById/<int:post_index>", views.PostRetriveUpdateDeleteView.as_view(), name="class_based_by_id"),
    path("classBasedViewGenerics/", views.PostGenericListCreateView.as_view(), name="class_based_list_posts_generics"),
    path("classBasedViewGenericsById/<int:pk>", views.PostGenericRetriveUpdateDeleteView.as_view(), name="class_based_by_id_generics"),

    path("<int:post_index>", views.get_post_by_id, name="number_via_url"),
    path("update/<int:post_index>", views.update_post_by_id, name="update_post"),
    path("delete/<int:post_index>", views.delete_post_by_id, name="delete_post"),
    path("post_for_current_user/", views.ListPostsForAuthor.as_view(), name="post_for_current_user"),
    path("post_for/<user_name>", views.ListPostsForAuthorQuery.as_view(), name="post_for_current_user"),
    path("post_for/", views.ListPostsForAuthorQueryParams.as_view(), name="post_for_current_user"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
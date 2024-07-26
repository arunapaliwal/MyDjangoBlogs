from django.urls import path
from . import views

urlpatterns = [
    path("",views.StartingPageView.as_view(),name="starting-page"),
    path("posts",views.PostPageView.as_view(),name="posts-page"),
    path("posts/<slug>",views.SinglePostView.as_view(),
         name="post-detail-page"),
    path("read-later",views.ReadLater.as_view(),name="read-later"),
    path("add-post",views.AddPostView.as_view(),name="add-post"),
    path('thank-you',views.ThankkYouView.as_view(),name="thank-you")
]

from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as get_yasg_schema_view
from drf_yasg import openapi
from django.contrib import admin
from . import views



schema_view = get_yasg_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API endpoints",
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    path('create-post/', views.CreatePostAPIView.as_view(), name='create-post'),
    path('posts/', views.ListPostAPIView.as_view(), name='list-posts'),
    path('my-posts/', views.MyPostsAPIView.as_view(), name='my-posts'),
    path('posts/<int:id>/', views.RetrievePostAPIView.as_view(), name='retrieve-post'),
    path('posts/<int:id>/update/', views.UpdatePostAPIView.as_view(), name='update-post'),
    path('posts/<int:id>/delete/', views.DestroyPostAPIView.as_view(), name='delete-post'),
    path('comments/<int:id>/', views.CommentAPIView.as_view(), name='comment-detail'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]

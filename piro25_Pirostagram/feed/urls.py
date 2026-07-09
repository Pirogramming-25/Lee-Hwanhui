from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),

    path('comment/<int:pk>/edit/', views.comment_update, name='comment_update'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    path('story/create/', views.story_create, name='story_create'),
    path('story/<int:pk>/', views.story_view, name='story_view'),

    path('search/users/', views.user_search, name='user_search'),
    path('search/posts/', views.post_search, name='post_search'),

    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
]
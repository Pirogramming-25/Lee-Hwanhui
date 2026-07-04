from django.urls import path
from . import views  

app_name = 'ideas'   

urlpatterns = [
    
    path('', views.idea_list, name='idea_list'),                   
    path('new/', views.idea_create, name='idea_create'),            
    path('<int:pk>/', views.idea_detail, name='idea_detail'),       
    path('<int:pk>/edit/', views.idea_update, name='idea_update'),  
    path('<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('<int:pk>/star/', views.idea_star_toggle, name='idea_star_toggle'),
    
    path('<int:pk>/interest/', views.idea_interest_update, name='idea_interest_update'),
    

    
    path('devtools/', views.devtool_list, name='devtool_list'),
    path('devtools/new/', views.devtool_create, name='devtool_create'),
    path('devtools/<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('devtools/<int:pk>/edit/', views.devtool_update, name='devtool_update'),
    path('devtools/<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),
]
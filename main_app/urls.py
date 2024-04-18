from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news_by_category/<str:category>/', views.news_by_category, name='news_by_category'),
    path('news_detail/<int:news_id>/', views.news_detail, name='news_detail'),
    path('add_comment/<int:news_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('create_news/', views.create_news, name='create_news'),
    path('edit_news/<int:news_id>/', views.edit_news, name='edit_news'),
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
    path('signup/', views.signup, name='signup'),
    path('user/<int:user_id>/', views.user_news, name='user_news'),
]

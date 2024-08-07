from django.urls import path
from . import views

urlpatterns = [
    path('news/<int:article_id>/comment/', views.add_comment, name='create_comment'),
    path('', views.news_home, name='news_home'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    # path('<int:pk>/update/', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news-delete'),
    path('search/', views.search, name='search'),
    path('news/<int:id>/', views.article_detail, name='article_detail'),
    path('news/category/<int:category_id>/', views.news_by_category, name='news-by-category'),
    path('news/<int:article_id>/edit/', views.edit, name='edit'),

]
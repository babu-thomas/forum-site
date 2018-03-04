from django.urls import path

from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('boards/<int:pk>/', views.BoardDetailView.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('boards/<int:pk>/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
]

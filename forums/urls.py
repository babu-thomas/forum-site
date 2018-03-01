from django.urls import path

from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home')
]

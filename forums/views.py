from django.views.generic import ListView, DetailView

from .models import Board


class BoardListView(ListView):
    template_name = 'home.html'
    model = Board


class BoardDetailView(DetailView):
    template_name = 'topics.html'
    model = Board

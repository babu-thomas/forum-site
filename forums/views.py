from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Board


class BoardListView(ListView):
    template_name = 'home.html'
    model = Board


class BoardDetailView(DetailView):
    template_name = 'topics.html'
    context_object_name = 'board'
    model = Board


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    context = {'board': board}
    return render(request, 'new_topic.html', context)

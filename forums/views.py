from django.views.generic import ListView

from .models import Board


class BoardListView(ListView):
    template_name = 'home.html'
    model = Board

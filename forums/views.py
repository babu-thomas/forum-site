from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from users.models import CustomUser as User
from .forms import NewTopicForm
from .models import Board, Post


class BoardListView(ListView):
    template_name = 'home.html'
    model = Board


class BoardDetailView(DetailView):
    template_name = 'topics.html'
    context_object_name = 'board'
    model = Board


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # TODO: Replace with currently logged in user
    user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user,
            )
            # TODO: Redirect to created topic page
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()

    context = {'board': board, 'form': form}
    return render(request, 'new_topic.html', context)

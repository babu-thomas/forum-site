from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import NewTopicForm, PostForm
from .models import Board, Post, Topic


class BoardListView(ListView):
    template_name = 'home.html'
    model = Board


class BoardDetailView(DetailView):
    template_name = 'board_topics.html'
    context_object_name = 'board'
    model = Board


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user

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
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()

    context = {'board': board, 'form': form}
    return render(request, 'new_topic.html', context)


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    context = {'topic': topic}
    return render(request, 'topic_posts.html', context)


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    context = {'topic': topic, 'form': form}
    return render(request, 'reply_topic.html', context)

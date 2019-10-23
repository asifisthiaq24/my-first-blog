from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

#import sqlite3

# def db_operation():
#     conn = sqlite3.connect('./db.sqlite3')
#     # print "Opened database successfully"
#     cursor = conn.execute("SELECT * from auth_user")
#     # print cursor
#     # for row in cursor:
#     #     print row[0]
#     #     print row[1]
#     #     print row[2]
#     #     print row[10]
#     # print "Operation done successfully"
#     conn.close()


# Create your views here.
import numpy as np
import pandas as pd
import json

def panda_testing():
    df = pd.DataFrame({'A': 1.,
                       'B': [211,211,1111,2],
                       'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                       'D': np.array([3] * 4, dtype='int32'),
                       'E': pd.Categorical(["test", "train", "test", "train"]),
                       'F': 'foo'})
    print 'printing data frame'
    print df

    ##
    df_json_split = df.to_json(orient='split')
    print df_json_split
    df_json_records = df.to_json(orient='records')
    print '\n\n\n\n'
    print df_json_records
    print 'sss'

    formatted_obj = json.dumps(df_json_split, indent=4, separators=(',', ': '))
    print(formatted_obj)

    data_top = df.head(1) 
    print '\n\n'
    print data_top
    print list(df.columns)
    print df.get(list(df.columns))
    for col in df.columns: 
        print col


# '{"columns": ["col 1", "col 2"],
#   "index": ["row 1", "row 2"],
#   "data": [["a", "b"], ["c", "d"]]}'
##


def home(request):
    # db_operation()
    return render(request, 'blog/home.html', {})


@login_required
def fifa_home(request):
    panda_testing()
    return render(request, 'blog/fifa_main.html', {})


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'pk': pk})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form, 'pk': pk})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

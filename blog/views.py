from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponseRedirect, HttpResponse)
from django.views.decorators.csrf import csrf_exempt

import numpy as np
import pandas as pd
import json
import sqlite3

def color_negative_red(value):
    """
    Colors elements in a dateframe
    green if positive and red if
    negative. Does not color NaN
    values.
    """
    color=''
    if value == 'Asia':
        color = 'red'
    elif value =='Europe':
        color = 'green'
    elif value == 'North America':
        color = 'black'
    elif value == 'Cereal':
        color ='blue'
    elif value =='Fruits':
        color = 'red'
    elif value =='Bihar':
        color = 'purple'
    elif value == 'AP':
        color = 'blue'

    return 'background-color: %s'  %color

def getDF():
    df = pd.read_csv('1k.csv')
    style_json = {
        "Units Sold":'text-align:right;color:white;background-color:black;',
        "Order Date":'text-align:center;color:white;background-color:purple;',
        "Others":{
            "Offline":'background-color:red;color:#000',
            "Online":'background-color:green;color:#000'
        }
    }
    df = df[['Region', 'Country', 'Item Type','Sales Channel','Order Date','Units Sold']].head(100)
    x=df.style.apply(lambda x:apply_styles_to_dataframe(x,style_json), axis=None)
    x = x.set_table_attributes('class="table table-bordered table-hover"')
    return x.hide_index().render(uuid='my_id')
####################################################
def apply_styles_to_dataframe(val,style_json):
    df = val.copy()
    for key in style_json:
        if key != 'Others':
            index=0
            for v in val.loc[:,key]:
                df.loc[index,key] = style_json[key]
                index = index+1
        elif key == 'Others':
            for col_name in val.loc[:,:]:
                for inner_key in style_json[key]:
                    matching_list = list(val.loc[val[col_name]==inner_key].index.values)
                    if matching_list != []:
                        for idx in matching_list:
                            df.loc[idx,col_name] = style_json[key][inner_key]
    return df  
def getDF_temp():
    conn = sqlite3.connect('./db.sqlite3')
    df = pd.read_sql_query("SELECT * FROM demo_data_tbl limit 150", conn)
    style_json = {
        "Name": 'text-align:right;color:white;background-color:black;',
        "Phone": 'text-align:center;color:black;background-color:#eee;',
        "Email": 'text-align:center',
        "Region": 'text-align:right',
        "Others": {
            "Bihar": 'background-color:red;color:#000;text-align:center',
            "AP": 'background-color:green;color:#000;',
            "UP": 'background-color:#efef44;color:#000;text-align:right'
        }
    }    
    x=df.style.apply(lambda x:apply_styles_to_dataframe(x,style_json), axis=None)
    #x = df.style.applymap(color_negative_red, subset=['Region'])
    x = x.set_table_attributes('class="table table-bordered table-hover"')
    return x.hide_index().render(uuid='my_id')

@csrf_exempt
def __pagination(request):
    # draw = request.POST['draw']
    start = int(request.POST['start'])
    length = int(request.POST['length'])
    print start
    print length
    search_val = str(request.POST['search[value]'])
    print search_val
    # if not len(search_val):
    #     search_val = '%'
    # else:  search_val = '%'+str(search_val)+'%'
    data = db_select("SELECT * FROM demo_data_tbl limit '"+str(length)+"' offset '"+str(start)+"'")
    filtered_count = len(data)
    #print data
    return HttpResponse(json.dumps({
        #"draw": draw,
        "recordsTotal": 200,
        "recordsFiltered": 200,
        "data": data,
            }))

def test(request):
    bytes = getDF_temp().encode('utf-8')
    return HttpResponse(bytes, content_type='application/json')

def db_select(query):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data
#####################################

def home(request):
    # db_operation()
    return render(request, 'blog/home.html', {})
@login_required
def fifa_home(request):
    #panda_testing()
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



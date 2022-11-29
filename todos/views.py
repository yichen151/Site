from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Grouping, Todo
from .forms import GroupForm, TodoForm


def check_grouping_owner(request, grouping):
    # 核实主题关联到的用户为当前登录的用户。
    if grouping.owner != request.user:
        raise Http404


def index(request):
    """Todo 的主页"""
    return render(request, 'todos/index.html')


@login_required
def groupings(request):
    """显示所有分组"""
    groupings = Grouping.objects.filter(owner=request.user).order_by('date_added')
    context = {'groupings': groupings}
    return render(request, 'todos/groupings.html', context)


@login_required
def grouping(request, grouping_id):
    """显示单个分组及其所有的 todo"""
    grouping = Grouping.objects.get(id=grouping_id)
    check_grouping_owner(request, grouping)
    todos = grouping.todo_set.order_by('-date_added')
    context = {'grouping': grouping, 'todos': todos}
    return render(request, 'todos/grouping.html', context)


@login_required
def new_grouping(request):
    """添加新分组"""
    if request.method != 'POST':
        # 未提交数据就创建一个新表单
        form = GroupForm()
    else:
        # 对 POST 提交的数据进行处理
        form = GroupForm(data=request.POST)
        if form.is_valid():
            new_grouping = form.save(commit=False)
            new_grouping.owner = request.user
            new_grouping.save()
            return redirect('todos:groupings')

    # 显示空白表单或指出表单无效。
    context = {'form': form}
    return render(request, 'todos/new_grouping.html', context)


@login_required
def new_todo(request, grouping_id):
    """在特定的分组中添加新 todo """
    grouping = Grouping.objects.get(id=grouping_id)
    check_grouping_owner(request, grouping)

    if request.method != 'POST':
        # 未提交数据就创建一个空表单
        form = TodoForm()
    else:
        # 对 POST 提交的数据进行处理
        form = TodoForm(data=request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.grouping = grouping
            new_todo.save()
            return redirect('todos:grouping', grouping_id=grouping_id)

    # 显示空表单或指出表单数据无效
    context = {'grouping': grouping, 'form': form}
    return render(request, 'todos/new_todo.html', context)


@login_required
def edit_todo(request, todo_id):
    """编辑已有的 todo """
    todo = Todo.objects.get(id=todo_id)
    grouping = todo.grouping
    check_grouping_owner(request, grouping)

    if request.method != 'POST':
        # 初次请求：使用已有的 todo 信息填充表单
        form = TodoForm(instance=todo)
    else:
        # 处理 POST 提交的数据
        form = TodoForm(instance=todo, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos:grouping', grouping_id=grouping.id)

    context = {'todo': todo, 'grouping': grouping, 'form': form}
    return render(request, 'todos/edit_todo.html', context)


@login_required
def edit_grouping(request, grouping_id):
    """编辑已有的 grouping"""
    grouping = Grouping.objects.get(id=grouping_id)
    check_grouping_owner(request, grouping)

    if request.method != 'POST':
        # 初次请求：使用已有的分组信息填充表单
        form = GroupForm(instance=grouping)
    else:
        # 处理 POST 提交的数据
        form = GroupForm(instance=grouping, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos:groupings')

    context = {'grouping': grouping, 'form': form}
    return render(request, 'todos/edit_grouping.html', context)


@login_required
def delete_todo(request, todo_id):
    """删除条目。"""
    todo = Todo.objects.get(id=todo_id)
    grouping = todo.grouping
    todo.delete()

    return redirect('todos:grouping', grouping_id=grouping.id)


@login_required
def delete_grouping(request, grouping_id):
    """删除分组。"""
    grouping = Grouping.objects.get(id=grouping_id)
    grouping.delete()

    return redirect('todos:groupings')

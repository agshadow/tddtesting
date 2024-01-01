from django.shortcuts import render, get_object_or_404
from task.models import Task
from task.forms import NewTaskForm, UpdateTaskForm
from django.shortcuts import redirect
from django.views.generic import ListView


def index(request):
    tasks = Task.objects.all()
    data = {
        'tasks': tasks
    }
    return render(request, 'task/index.html',data)

def detail(request, pk):
    task = Task.objects.get(pk=pk)
    data = {
        'task': task
    }
    return render(request, 'task/detail.html',data)

def new(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else: #GET
        form = NewTaskForm()

    data = {
        'form': form
    }
    return render(request, 'task/new.html', data)


def update(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == "POST":
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    else: #GET
        form = UpdateTaskForm(instance=task)

    data = {
        'form': form
    }
    return render(request, 'task/update.html', data)

def delete(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    return redirect('index')


class TaskListView(ListView):
    model = Task
    template_name = 'task/listtask.html'
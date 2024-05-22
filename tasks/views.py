from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages

from .models import Task, Tag
from .forms import TaskForm, TagForm, UserRegisterForm


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    tasks = Task.objects.filter(user=request.user).order_by("is_done", "-created_at")
    return render(request, "tasks/home.html", {"tasks": tasks})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Your account has been created! You are now able to log in")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "tasks/register.html", {"form": form})

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect("home")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect("home")

@login_required
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect("home")

@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "tasks/tag_list.html", {"tags": tags})

@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect("tag_list")
    else:
        form = TagForm()
    return render(request, "tasks/tag_form.html", {"form": form})

@login_required
def update_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect("tag_list")
    else:
        form = TagForm(instance=tag)
    return render(request, "tasks/tag_form.html", {"form": form})

@login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return redirect("tag_list")


class TaskListView(ListView):
    model = Task
    template_name = "tasks/home.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-created_at")

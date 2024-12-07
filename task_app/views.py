from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse,  HttpResponseRedirect
from django.urls import reverse
from .models import *


class LoginView(TemplateView):
    template_name = "login.html"
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('task_list'))
    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('task_list'))
        return render(request, self.template_name, locals())

class LogoutView(TemplateView):
    def post(self, request):
        return HttpResponse('logout')

class TasksListView(TemplateView):
    template_name = 'task_list.html'
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user)
            print(tasks, '------')
            return render(request, self.template_name, locals())
        return HttpResponseRedirect(reverse('google_login'))


class CreateTaskView(TemplateView):
    template_name = 'task_create.html'
    def post(self, request):
        if request.user.is_authenticated:
            task = Task.objects.create(
                title=request.POST["title"],
                description=request.POST["description"],
                user=request.user
            )
            return HttpResponseRedirect(reverse('task_list'))
        return HttpResponseRedirect(reverse('google_login'))

class EditTaskView(TemplateView):
    template_name = 'task_edit.html'
    def get(self, request, id):
        task = Task.objects.get(id=id)
        return render(request, self.template_name, locals())
    def post(self, request, id):
        task = Task.objects.get(id=id)
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.is_completed = True if 'is_completed' in request.POST else False
        task.save()
        return HttpResponseRedirect(reverse('task_list'))

class DeleteTaskView(TemplateView):
    def get(self, request, id):
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponseRedirect(reverse('task_list'))

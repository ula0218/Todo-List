from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.http import HttpRequest, HttpResponse
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
# LoginRequiredMixin 強制用戶訪問某試圖前需要先登入，如未登入會導向登入頁面
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



# Class-based views

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    next_page = reverse_lazy('tasks:tasks')
    # def get_success_url(self):
    #     return reverse_lazy('tasks:tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class =UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks:tasks')
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            # 從表單中獲取了用戶對象，把其保存到了用戶變數中，然後使用了這個變數來進行登錄
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        # 當前用戶已登入的話，重定向到任務頁面
        if self.request.user.is_authenticated:
            return redirect('tasks:tasks')
        # 用戶沒有登錄，將會執行RegisterPage的父類別(即FormView)之get方法，會渲染註冊頁面並傳回給用戶
        return super(RegisterPage,self).get( *args, **kwargs)


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    # queryset 
    context_object_name = 'tasks'

    # def get_queryset(self):
    #     # 過濾 queryset 以過濾出和當前用戶相關的任務
    #     queryset = super().get_queryset()
    #     return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            #保留標題以該搜尋關鍵字開頭的任務
            context['tasks'] = context['tasks'].filter(
                title__startswith =search_input
            )
        context['search-input'] = search_input
        return context # 篩選後的任務列表、未完成任務的數量以及搜尋關鍵字

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks:tasks')
    # 處理表單驗證成功情況
    def form_valid(self, form):
        # 將表單實例的用戶欄位設定為目前請求的用戶
        form.instance.user = self.request.user
        # 獲取TaskCreate類別的父類別（即CreateView）的form_valid()方法
        # 確定在表單驗證成功時，父類別中定義的預設行為也能得以執行。
        return super(TaskCreate,self).form_valid(form)
    

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks:tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:tasks')


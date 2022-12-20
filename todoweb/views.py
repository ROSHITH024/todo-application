from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView
from todoweb.form import UserRegistration,LoginForm,TodoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todoapp.models import Todos
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"You must log in")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

class RegisterView(CreateView):
    template_name="register.html"
    form_class=UserRegistration
    model=User
    success_url=reverse_lazy("signin")
    # def get(self,req,*args,**kw):
    #     form=UserRegistration()
    #     return render(req,"register.html",{"form":form})
    # def post(self,req,*args,**kw):
    #     form=UserRegistration(req.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(req,'Account Created')
    #         return redirect("signin")
    #     else:
    #         messages.error(req,'Account not created')
    #         return render(req,"register.html",{"form":form})

class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm

    # def get(self,req,*args,**kw):
    #     form=LoginForm()
    #     return render(req,"login.html",{"form":form})

    def post(self,req,*args,**kw):
        form=LoginForm(req.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            usr=authenticate(req,username=uname,password=pwd)
            print(f"user={usr}")
            if usr:
                login(req,usr)
                return redirect("home")
            else:
                messages.error(req,'Invalid username or password')
                print("invalid user")
                return redirect("signin")
@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    template_name="index.html"
    # def get(self,request,*args,**kw):
    #     return render(render,"index.html")

@method_decorator(signin_required,name="dispatch")
class TodoListView(ListView):
    template_name="todo-list.html"
    model=Todos
    context_object_name="todos"

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    # def get(self,request,*args,**kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     return render(request,"todo-list.html",{"todos":qs})

@method_decorator(signin_required,name="dispatch")
class TodoCreateView(CreateView):
    template_name="todo-add.html"
    form_class=TodoForm
    model=Todos
    success_url=reverse_lazy("alltodos")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    # def get(self,req,*args,**kw):
    #     form=TodoForm()
    #     return render(req,"todo-add.html",{"form":form})

    # def post(self,req,*args,**kw):
    #     form=TodoForm(req.POST)
    #     if form.is_valid():
    #         instance=form.save(commit=False)
    #         instance.user=req.user
    #         instance.save()
    #         messages.success(req,'Todo Created Succesfully')
    #         return redirect("alltodos")
    #     else:
    #         messages.error(req,'Todo not Created')
    #         return render(req,"todo-add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class TodoDetail(DetailView):
    template_name="todo-detail.html"
    model=Todos
    context_object_name="todo"
    pk_url_kwarg="id"
    
    # def get(self,req,*args,**kw):
    #     id=kw.get("id")
    #     qs=Todos.objects.get(id=id)
    #     return render(req,"todo-detail.html",{"todo":qs})

@signin_required
def todo_delete_view(req,*args,**kw):
    id=kw.get("id")
    Todos.objects.get(id=id).delete()
    return redirect("alltodos")
@signin_required
def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("signin")
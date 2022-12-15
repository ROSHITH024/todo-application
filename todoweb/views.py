from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView
from todoweb.form import UserRegistration,LoginForm,TodoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from todoapp.models import Todos
# Create your views here.

class RegisterView(View):
    def get(self,req,*args,**kw):
        form=UserRegistration()
        return render(req,"register.html",{"form":form})
    def post(self,req,*args,**kw):
        form=UserRegistration(req.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("signup")
        else:
            return render(req,"register.html",{"form":form})

class LoginView(View):
    def get(self,req,*args,**kw):
        form=LoginForm()
        return render(req,"login.html",{"form":form})

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
                print("invalid user")
                return redirect("signin")

class IndexView(TemplateView):
    template_name="index.html"
    # def get(self,request,*args,**kw):
    #     return render(render,"index.html")

class TodoListView(View):
    def get(self,request,*args,**kw):
        qs=Todos.objects.filter(user=request.user)
        return render(request,"todo-list.html",{"todos":qs})

class TodoCreateView(View):
    def get(self,req,*args,**kw):
        form=TodoForm()
        return render(req,"todo-add.html",{"form":form})

    def post(self,req,*args,**kw):
        form=TodoForm(req.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=req.user
            instance.save()
            return redirect("alltodos")
        else:
            return render(req,"todo-add.html",{"form":form})

class TodoDetail(View):
    def get(self,req,*args,**kw):
        id=kw.get("id")
        qs=Todos.objects.get(id=id)
        return render(req,"todo-detail.html",{"todo":qs})

def todo_delete_view(req,*args,**kw):
    id=kw.get("id")
    Todos.objects.get(id=id).delete()
    return redirect("alltodos")
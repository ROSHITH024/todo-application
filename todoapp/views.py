from multiprocessing import context
from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from todoapp.models import Todos
from todoapp.serializer import TodoSerializer,RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import authentication,permissions
# Create your views here.


class TodosView(ViewSet):
    def list(self,requst,*args,**kw):
        qs=Todos.objects.all()
        sr=TodoSerializer(qs,many=True)
        return Response(data=sr.data)
    def create(self,request,*args,**kw):
        sr=TodoSerializer(data=request.data)
        if sr.is_valid():
            sr.save()
            return Response(data=sr.data)
        else:
            return Response(data=sr.errors)
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        sr=TodoSerializer(qs,many=False)
        return Response(data=sr.data)
    def destroy(self,request,*args,**kw):
        t_id=kw.get("pk")
        Todos.objects.get(id=t_id).delete()
        return Response(data="Data deleted")
    def update(self,request,*args,**kw):
        t_id=kw.get("pk")
        obj=Todos.objects.get(id=t_id)
        sr=TodoSerializer(data=request.data,instance=obj)
        if sr.is_valid():
            sr.save()
            return Response(data=sr.data)
        else:
            return Response(sr.errors)


class TodoModelViewset(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()

    def create(self,request,*args,**kw):
        sr=TodoSerializer(data=request.data,context={"user":request.user})
        if sr.is_valid():
            sr.save()
            return Response(data=sr.data)
        else:
            return Response(data=sr.errors)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False,user=request.user)
        sr=TodoSerializer(qs,many=True)
        return Response(data=sr.data)

    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True,user=request.user)
        sr=TodoSerializer(qs,many=True)
        return Response(data=sr.data)

    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        obj=Todos.objects.get(id=id)
        obj.status=True
        obj.save()
        sr=TodoSerializer(obj,many=False)
        return Response(data=sr.data)
#localhost:8000/api/v1/todos/2/mark_as_done/
# post        

class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self, request, *args, **kwargs):
    #     sr=RegistrationSerializer(data=request.data)
    #     if sr.is_valid():
    #         User.objects.create_user(**sr.validated_data)
    #         return Response(data=sr.data)
    #     else:
    #         return Response(data=sr.errors)
      
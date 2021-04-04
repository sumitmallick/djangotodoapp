from django.shortcuts import render, redirect
from basic_app.forms import *
from .models import Todo
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.views.decorators.csrf import csrf_exempt
from .serializers import TodoSerializer, UserSerializer

#send email
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


@login_required
def addTodo(request):
    form1 = TodoForm()

    if request.method == 'POST':
        form1 = TodoForm(request.POST or None)

        print(form1.errors)

        if form1.is_valid():
            obj = form1.save(commit=False)
            print(request.user)
            obj.uid = request.user
            obj.save()
            subject = 'New Todo: '+form1.cleaned_data['title']
            message = 'You have created a new todo item which is scheduled for '+str(form1.cleaned_data['scheduled_time'])
            from_email = settings.EMAIL_HOST_USER
            to_list = [request.user.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            messages.success(request,('Item has been added to list.'))
            return redirect('basic_app:todos',pk=request.user.pk)

    context = {
        'form1':form1
    }
    return render(request,'add_todo.html',context=context)


#--------------------------------------------------------------------------------#


@login_required
def todos(request,pk):
    data1 = Todo.objects.filter(uid__pk=pk)


    context = {
        'data1':data1
    }

    return render(request,'todos.html',context=context)


#--------------------------------------------------------------------------------#



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:user_login'))


#--------------------------------------------------------------------------------#




def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('basic_app:todos',pk=user.pk)
            else:
                print("Account not active")

        else:
            return HttpResponse("Invalid login details")




    return render(request,'login.html')


#--------------------------------------------------------------------------------#




def register(request):


    form1 = UserForm()


    if request.method == 'POST':
        form1 = UserForm(data=request.POST)

        if form1.is_valid():

            data1 = form1.save()
            data1.set_password(data1.password)
            data1.save()
            return HttpResponseRedirect(reverse('basic_app:user_login'))


        else:
            print(form1.errors)



    context = {
            'form1':form1

        }




    return render(request, 'register.html',context=context)




#--------------------------------------------------------------------------------#





def delete(request,pk):
    data = Todo.objects.get(pk=pk)
    data.delete()
    messages.success(request,('Item has been deleted.'))
    return redirect('basic_app:todos',pk=request.user.pk)



#--------------------------------------------------------------------------------#





def done(request,pk):
    data = Todo.objects.get(pk=pk)
    data.completed = True
    data.save()
    messages.success(request,(str(data.title)+' status set to done.'))
    return redirect('basic_app:todos',pk=request.user.pk)




#--------------------------------------------------------------------------------#





def undone(request,pk):
    data = Todo.objects.get(pk=pk)
    data.completed = False
    data.save()
    messages.success(request,(str(data.title)+' status set to undone.'))
    return redirect('basic_app:todos',pk=request.user.pk)



#--------------------------------------------------------------------------------#



def edit(request,pk):

    if request.method == 'POST':
        data = Todo.objects.get(pk=pk)

        form = TodoForm(request.POST or None, instance=data)
        # return HttpResponse(form.errors)
        if form.is_valid():


            obj = form.save(commit=False)
            print(request.user)
            obj.uid = request.user
            obj.save()

            messages.success(request,('Item has been edited.'))
            return redirect('basic_app:todos',pk=request.user.pk)

    else:
        form = TodoForm()
        data = Todo.objects.get(pk=pk)
        return render(request,'edit.html',{'form':form, 'data':data})



#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

    #RESTFUL API USING GENERIC CLASS BASED VIEWS
#_____________________________________________________#

#Token based Login API
@csrf_exempt
@api_view(['POST'])
def APIlogin(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error':'Please provide both username and password'},
            status = status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username,password=password)

    if not user:
        return Response({'error':'Invalid username or password'},
            status = status.HTTP_404_NOT_FOUND
        )
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token':token.key,
                     'username':user.username,
                     'email':user.email

                    },
        status=status.HTTP_200_OK)



#--------------------------------------------------------------------------------#



#API to get all todos or to create a new todo
class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)



#--------------------------------------------------------------------------------#



#API to get all todos or to create a new todo
class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)



#--------------------------------------------------------------------------------#


#Resful API for user registration
@csrf_exempt
@api_view(['POST'])
def RegisterAPIView(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        print(request.data)
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



#--------------------------------------------------------------------------------#


#Resful API to mark todo TRUE / FALSE
class MarkTodoAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def post(self,request,pk):
        data1 = Todo.objects.get(pk=pk)
        data1.completed = not data1.completed
        data1.save()
        data2 = Todo.objects.get(pk=pk)
        data3 = TodoSerializer(data2)
        return Response(data3.data,status=status.HTTP_201_CREATED)

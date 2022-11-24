from .models import Role
from django.shortcuts import redirect
from django.http import HttpResponse

def admin_required(function):
    def wrap(*args, **kwargs):
        print(args[0].user)
        print(args[0].user.role.role)
        if args[0].user.role.role == 'admin':
            return function(*args, **kwargs)
        else:
          return redirect('login_user')
    return wrap

def profesor_required(function):
    def wrap(*args, **kwargs):
        print(args[0].user)
        print(args[0].user.role.role)
        if args[0].user.role.role == 'prof':
            return function(*args, **kwargs)
        else:
          return redirect('login_user')
    return wrap


def student_required(function):
    def wrap(*args, **kwargs):
        #print(args[0].user)
        #print(args[0].user.role.role)
        if args[0].user.role.role == 'stud' and args[0].user.status.status == 'red':
            return function(*args, **kwargs)
        elif args[0].user.role.role == 'stud' and args[0].user.status.status == 'izvan':
          return function(*args, **kwargs)
        else:
          return redirect('login_user')
    return wrap

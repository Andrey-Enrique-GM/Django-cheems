from django.shortcuts import render
from .entities.user import User



def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})

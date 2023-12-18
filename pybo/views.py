from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    return render(request, 'index.html')

def map(request):
    return render(request, 'map.html')

def data(request):
    return render(request, 'data.html')



def files(request):
    return render(request, 'etc/files_list.html')
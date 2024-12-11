from django.shortcuts import render


def index(request):
    return render(request, 'adunix/index.html')

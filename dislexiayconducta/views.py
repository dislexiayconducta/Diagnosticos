from django.shortcuts import render


def welcome(request):
    return render(request, "dislexiayconducta/welcome.html")

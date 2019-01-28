from django.shortcuts import render

def conirmationWindow(request, *args, **kwargs):
    return render(request, 'windows/confirmation_window.html', {'message' : kwargs['message']})
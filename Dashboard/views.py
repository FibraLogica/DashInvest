from django.shortcuts import render

def dashboard(request):
    return render(request, 'front_end/dashboard.html')
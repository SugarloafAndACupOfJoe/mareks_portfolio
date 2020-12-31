from django.shortcuts import render


def welcome(request):
    context = {
        'page': request.path
    }
    return render(request, 'airpollution/welcome.html', context)

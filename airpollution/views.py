from django.shortcuts import render


def welcome(request):
    context = {
        'view_name': request.resolver_match.view_name
    }
    return render(request, 'airpollution/welcome.html', context)

from django.shortcuts import render
from website.models import MyApp


# Create your views here.
def index(request):
    all_apps = MyApp.objects.all()
    context = {
        'my_apps': all_apps,
        'app_name': request.resolver_match.app_name
    }
    return render(request, 'website/index.html', context)

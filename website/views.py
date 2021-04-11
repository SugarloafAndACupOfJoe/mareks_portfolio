from django.shortcuts import render
from website.models import MyApp


# Create your views here.
def index(request):
    return render(request, 'website/index.html')


def samples(request):
    return render(request, 'website/samples.html')

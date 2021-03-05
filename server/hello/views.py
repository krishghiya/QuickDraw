from django.http import HttpResponse

def home(request):
    print(request)
    return HttpResponse("Hello, Django!")

def predict(request):
    print(request)
    return HttpResponse("Success!") 
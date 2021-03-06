from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
# import tensorflow as tf

def home(request):
    print(request)
    return HttpResponse("Hello, Django!")

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        lines = json.loads(json.loads(request.body)['lines'])['lines']
        lines = [l['points'][1:-1] for l in lines]
        points = []
        for l in lines:
            for d in l:
                points.append([d['x'], d['y'], 0])
            points[-1][-1] = 1

        return HttpResponse("Success!")
    else:
        return HttpResponse("GET Request invalid!") 
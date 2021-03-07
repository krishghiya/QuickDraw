from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import pickle
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf

model = tf.keras.models.load_model(os.path.split(os.getcwd())[0] + '\model')
names = pickle.load(open('hello/names.pickle', 'rb'))

def home(request):
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
        
        points = np.array(points)
        # initial_plot_image(points)

         # Preprocessing.
         # 1. Size normalization.
        lower = np.min(points[:, 0:2], axis=0)
        upper = np.max(points[:, 0:2], axis=0)
        scale = upper - lower
        scale[scale == 0] = 1
        points[:, 0:2] = (points[:, 0:2] - lower) / scale
        # 2. Compute deltas.
        points[1:, 0:2] -= points[0:-1, 0:2]
        np_ink = points[1:, :].reshape(1, -1, 3)

        # plot_image(np_ink[0])

        results = model.predict(np_ink)
        values, indices = tf.nn.top_k(results[0], k=3)
        indices = indices.numpy() 
        indices = [names[i] for i in indices]
        values = values.numpy() * 100
        str_values = [{'name': x.title(), 'confidence': str(round(y, 2))} 
                    for x, y in zip(indices, values)]

        return HttpResponse(json.dumps(str_values))
    else:
        return HttpResponse("GET Request invalid!") 

def plot_image(ink):
    import matplotlib.pyplot as plt
    origin_points = [[0., 0., 0.]]
    points = np.r_[origin_points, ink]
    line_indices = np.argwhere(points[:, -1])[:,0]
    coordinates = np.cumsum(points[:, :2], axis=0)
    strokes = np.split(coordinates, line_indices + 1)
    plt.scatter(coordinates[:, 0], -coordinates[:, 1], marker='.')
    
    for stroke in strokes:
        plt.plot(stroke[:, 0], -stroke[:, 1])

    plt.axis("off")
    plt.show()

def initial_plot_image(points):
    import matplotlib.pyplot as plt
    line_indices = np.argwhere(points[:, -1])[:,0]
    strokes = np.split(points[:, :2], line_indices + 1)
    plt.scatter(points[:, 0], -points[:, 1])

    for s in strokes:
        plt.plot(s[:, 0], -s[:, 1])
    
    plt.axis('off')
    plt.show()
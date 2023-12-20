import os
import time
from django.shortcuts import render

from ai.helpers import prccess_image

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        timeStarted = time.time()
        print(request.FILES['image'])
        image = request.FILES['image']

        fs = FileSystemStorage()
        if os.path.exists(f'media/{image.name}'):
            os.remove(f'media/{image.name}')
        
        filename = fs.save(image.name, image)

        image_path = fs.url(filename)
        dominant_colors_url, plot_url, optimal_k = prccess_image(image_path)

        time_taken = time.time() - timeStarted
        return render(
            request, 'result.html',
            {
                'dominant_colors_url': dominant_colors_url,
                'plot_url': plot_url,
                'optimal_k': optimal_k,
                'time_taken': f'{time_taken:.2f}'
            })

    return render(request, 'index.html')
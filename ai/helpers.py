import os
from PIL import Image
from django.conf import settings
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from yellowbrick.cluster import KElbowVisualizer
import uuid



def find_optimal_k(pixels):
    model = KMeans(random_state=0, n_init='auto')
    visualizer = KElbowVisualizer(model, k=(1, 5), timings=False)
    
    visualizer.fit(pixels)
    visualizer.set_title('Elbow Plot')
    
    if os.path.exists('media/plot.png'):
        os.remove('media/plot.png')
    
    visualizer.fig.savefig('media/plot.png')

    return visualizer.elbow_value_


def prccess_image(image_path):
    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
    image = Image.open(f"./{full_image_path}") 
    image_np = np.array(image)
    pixels = image_np.reshape(-1, 3)

    optimal_k = find_optimal_k(pixels) or 3

    # Apply K-means clustering with the optimal K
    kmeans = KMeans(n_clusters=optimal_k, n_init=5)

    kmeans.fit(pixels)

    # Get the RGB values of the cluster centers (dominant colors)
    dominant_colors = kmeans.cluster_centers_.astype(int)

    # Plot the dominant colors
    plt.figure(figsize=(8, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow([dominant_colors])
    plt.title(f'Dominant Colors (K={optimal_k})')
    plt.axis('off')
    
    # check if the file name already exists
    if os.path.exists('media/dominant_colors.png'):
        os.remove('media/dominant_colors.png')
    
    plt.savefig('media/dominant_colors.png')
 
    dominant_colors_url = os.path.join(settings.MEDIA_URL, 'dominant_colors.png')
    plot_url = os.path.join(settings.MEDIA_URL, 'plot.png')
    

    return dominant_colors_url, plot_url
    
    
    
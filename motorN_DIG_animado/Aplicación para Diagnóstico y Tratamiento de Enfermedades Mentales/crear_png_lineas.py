import numpy as np
import matplotlib.pyplot as plt

size = 50

# Líneas verticales gruesas
img_v = np.zeros((size, size), dtype=np.float32)
for i in range(0, size, 5):
    img_v[:, i:i+2] = 1.0  # líneas verticales de 2 píxeles de grosor
plt.imsave('png_lineas_verticales.png', img_v, cmap='gray')

# Líneas horizontales gruesas
img_h = np.zeros((size, size), dtype=np.float32)
for i in range(0, size, 5):
    img_h[i:i+2, :] = 1.0  # líneas horizontales de 2 píxeles de grosor
plt.imsave('png_lineas_horizontales.png', img_h, cmap='gray')

print('PNGs de líneas creados: verticales y horizontales')

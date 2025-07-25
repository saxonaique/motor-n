import numpy as np
import matplotlib.pyplot as plt

# Crear un patrón simple: cuadrado blanco sobre fondo negro
size = 50
img = np.zeros((size, size), dtype=np.float32)
img[15:35, 15:35] = 1.0  # cuadrado blanco en el centro

plt.imsave('png_muestra_inyeccion.png', img, cmap='gray')
print('PNG de muestra creado: png_muestra_inyeccion.png')

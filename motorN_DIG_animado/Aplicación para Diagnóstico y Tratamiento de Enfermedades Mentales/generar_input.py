import numpy as np
from scipy.io import wavfile

# Parámetros
TASA_MUESTREO = 44100
DURACION = 2  # segundos
FRECUENCIA = 5  # Hz (onda baja tipo "depresión")

# Generar señal seno
x = np.linspace(0, DURACION, int(TASA_MUESTREO * DURACION), endpoint=False)
senal = 0.5 * np.sin(2 * np.pi * FRECUENCIA * x)

# Normalizar a int16
senal_int16 = np.int16(senal / np.max(np.abs(senal)) * 32767)

# Guardar archivo WAV
wavfile.write('1_entrada_simulada_depresion.wav', TASA_MUESTREO, senal_int16)
print('Archivo de entrada generado: 1_entrada_simulada_depresion.wav')

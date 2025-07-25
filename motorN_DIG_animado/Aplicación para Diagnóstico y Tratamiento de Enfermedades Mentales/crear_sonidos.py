import numpy as np
import scipy.io.wavfile as wav

# Configuración de audio
TASA_MUESTREO = 44100  # Hz (calidad CD)
DURACION = 5  # segundos

# Función para generar la señal de depresión
def generar_eeg_depresivo(duracion, tasa_muestreo):
    """
    Genera una señal que simula un estado de depresión:
    - Dominio de ondas lentas (Theta/Delta: 1-8 Hz)
    - Baja variabilidad, patrones repetitivos
    - Poca actividad de alta frecuencia (ruido)
    """
    t = np.linspace(0, duracion, int(duracion * tasa_muestreo), False)
    
    # Componente principal: ondas lentas (depresión)
    señal_lenta = 0.7 * np.sin(2 * np.pi * 3 * t)  # 3 Hz (Delta)
    señal_lenta += 0.5 * np.sin(2 * np.pi * 6 * t)  # 6 Hz (Theta)
    
    # Ruido muy bajo para simular rigidez
    ruido = 0.1 * np.random.normal(0, 1, len(t))
    
    # Sin modulación de amplitud para simular falta de flexibilidad
    
    señal_depresiva = señal_lenta + ruido
    
    # Asegurar que la señal no exceda los límites antes de normalizar
    señal_depresiva = np.clip(señal_depresiva, -1.0, 1.0)
    
    return señal_depresiva

# Función para crear la contraonda para la depresión
def crear_contraonda_depresion(señal_original, tasa_muestreo):
    """
    Crea una contraonda para la depresión:
    - Introduce variabilidad y complejidad
    - Componentes de frecuencias más rápidas (Beta/Gamma) para activar/flexibilizar
    - Un tono audible para asegurar la percepción
    """
    t = np.linspace(0, DURACION, int(DURACION * tasa_muestreo), False)
    
    # Tono puro audible para asegurar la audibilidad
    tono_puro = 0.6 * np.sin(2 * np.pi * 440 * t) # 440 Hz (La 4)
    
    # Componentes de alta frecuencia para activar/flexibilizar
    activacion_beta = 0.3 * np.sin(2 * np.pi * 25 * t) # 25 Hz (Beta)
    activacion_gamma = 0.2 * np.sin(2 * np.pi * 50 * t) # 50 Hz (Gamma)
    
    # Ruido blanco atenuado para introducir complejidad y romper patrones
    ruido_activador = 0.1 * np.random.normal(0, 1, len(t))
    
    contraonda = tono_puro + activacion_beta + activacion_gamma + ruido_activador
    
    # Normalizar la contraonda para asegurar que use todo el rango dinámico
    contraonda = contraonda / np.max(np.abs(contraonda)) if np.max(np.abs(contraonda)) > 0 else contraonda
    
    return contraonda

# Generar la señal de depresión
print("Generando señal de depresión (baja entropía funcional)...")
señal_depresiva = generar_eeg_depresivo(DURACION, TASA_MUESTREO)

# Normalizar y convertir a formato de audio
señal_normalizada = señal_depresiva / np.max(np.abs(señal_depresiva)) if np.max(np.abs(señal_depresiva)) > 0 else señal_depresiva
señal_int16 = (señal_normalizada * 32767).astype(np.int16)

# Guardar el archivo de entrada
wav.write("1_entrada_simulada_depresion.wav", TASA_MUESTREO, señal_int16)
print("✓ Archivo \'1_entrada_simulada_depresion.wav\' creado.")

# Generar la contraonda para la depresión
print("Generando contraonda para la depresión (alta entropía funcional controlada)...")
contraonda = crear_contraonda_depresion(señal_depresiva, TASA_MUESTREO)

# Normalizar y convertir a formato de audio
contraonda_normalizada = contraonda / np.max(np.abs(contraonda)) if np.max(np.abs(contraonda)) > 0 else contraonda
contraonda_int16 = (contraonda_normalizada * 32767).astype(np.int16)

# Guardar el archivo de contraonda
wav.write("2_contraonda_depresion_activadora.wav", TASA_MUESTREO, contraonda_int16)
print("✓ Archivo \'2_contraonda_depresion_activadora.wav\' creado.")

print("\n🎵 Archivos de audio generados exitosamente.")
print("Puedes escuchar ambos archivos para comparar:")
print("- \'1_entrada_simulada_depresion.wav\': Sonido lento y repetitivo (depresión)")
print("- \'2_contraonda_depresion_activadora.wav\': Sonido más complejo y activador")


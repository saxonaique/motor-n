import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import rfft, irfft
import matplotlib.pyplot as plt

# --- PARÁMETROS GLOBALES DEL LABORATORIO ---
# Define las bandas de frecuencia de interés (en Hz)
# Ajustadas para el contexto de depresión/activación
BANDA_DEPRESION = (1, 8)    # Frecuencias Delta/Theta (asociadas a depresión)
BANDA_ACTIVACION = (15, 60) # Frecuencias Beta/Gamma (asociadas a activación/flexibilidad)
TASA_MUESTREO = 44100       # Estándar para audio de calidad CD

class LaboratorioN:
    """
    Un laboratorio para procesar señales de onda basado en principios
    de entropía y teoría de la información.
    """
    def __init__(self, tasa_muestreo=TASA_MUESTREO):
        self.tasa_muestreo = tasa_muestreo
        print("🔬 Laboratorio N inicializado.")
        print(f"Tasa de muestreo configurada a {tasa_muestreo} Hz.")
        # --- Motor N: campo 2D ---
        self.grid_size = 50
        self.resetear_campo()

    def evolucionar_campo(self, alpha=0.05):
        """
        Aplica una regla de difusión discreta: cada celda evoluciona hacia el promedio de su vecindario 3x3.
        """
        nuevo = self.campo.copy()
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                sub = self.campo[max(0, r - 1):min(self.grid_size, r + 2), max(0, c - 1):min(self.grid_size, c + 2)]
                avg = np.mean(sub)
                nuevo[r, c] += alpha * (avg - self.campo[r, c])
        self.campo = np.clip(nuevo, 0, 1)

    def calcular_varianza_local(self, r, c):
        """
        Calcula la varianza local 3x3 alrededor de la celda (r, c).
        """
        sub = self.campo[max(0, r - 1):min(self.grid_size, r + 2), max(0, c - 1):min(self.grid_size, c + 2)]
        avg = np.mean(sub)
        varianza = np.mean((sub - avg) ** 2)
        return varianza

    def get_campo(self):
        """
        Devuelve una copia del campo actual (para visualización).
        """
        return self.campo.copy()

    def resetear_campo(self):
        """
        Reinicia el campo con valores aleatorios bajos.
        """
        self.campo = np.random.rand(self.grid_size, self.grid_size) * 0.15

    def inyectar_patron_ansiedad(self):
        """
        Inyecta un patrón de alta intensidad (ansiedad) en el centro del campo.
        """
        centro = self.grid_size // 2
        radio = 5
        self.campo[centro-radio:centro+radio, centro-radio:centro+radio] = 1.0

    def calcular_metricas(self):
        """
        Calcula entropía, varianza y valor máximo del campo.
        Guarda el resultado en self.metricas_ultimas.
        """
        import numpy as np
        campo = self.campo
        # Entropía de Shannon
        hist, _ = np.histogram(campo, bins=20, range=(0,1), density=True)
        hist = hist[hist>0]
        entropia = -np.sum(hist * np.log2(hist)) if len(hist)>0 else 0.0
        varianza = np.var(campo)
        maximo = np.max(campo)
        self.metricas_ultimas = {
            'entropia': float(entropia),
            'varianza': float(varianza),
            'maximo': float(maximo)
        }
        return self.metricas_ultimas

    def exportar_estado(self, ruta):
        """
        Exporta el campo y métricas actuales a un archivo JSON.
        """
        import json
        self.calcular_metricas()
        data = {
            'campo': self.campo.tolist(),
            'metricas': self.metricas_ultimas
        }
        with open(ruta, 'w') as f:
            json.dump(data, f, indent=2)

    def importar_estado(self, ruta):
        """
        Importa el campo y métricas desde un archivo JSON.
        """
        import json
        with open(ruta, 'r') as f:
            data = json.load(f)
        if 'campo' in data:
            import numpy as np
            self.campo = np.array(data['campo'], dtype=float)
        if 'metricas' in data:
            self.metricas_ultimas = data['metricas']


    def encoder(self, nombre_archivo_wav):
        """
        Codificador: Lee una señal de audio desde un archivo .wav y la convierte
        en un formato que el campo N puede entender (un array de numpy).
        """
        print(f"\n[1. ENCODER] Cargando señal desde \'{nombre_archivo_wav}\'...")
        try:
            # Lee la frecuencia y los datos del archivo wav
            tasa_leida, datos_onda = wav.read(nombre_archivo_wav)
            
            # Asegura que la tasa de muestreo sea la esperada
            if tasa_leida != self.tasa_muestreo:
                print(f"Advertencia: La tasa de muestreo del archivo ({tasa_leida} Hz) es diferente a la del laboratorio ({self.tasa_muestreo} Hz). Esto puede afectar la calidad.")

            # Si el audio es estéreo, lo convierte a mono promediando los canales
            if datos_onda.ndim > 1:
                print("Señal estéreo detectada. Convirtiendo a mono.")
                datos_onda = datos_onda.mean(axis=1)
            
            # Normaliza la señal al rango [-1, 1] para un procesamiento consistente
            datos_normalizados = datos_onda / np.max(np.abs(datos_onda)) if np.max(np.abs(datos_onda)) > 0 else datos_onda
            print("Señal cargada y normalizada con éxito.")
            return datos_normalizados

        except FileNotFoundError:
            print(f"Error: El archivo \'{nombre_archivo_wav}\' no fue encontrado.")
            return None
        except Exception as e:
            print(f"Error al leer el archivo de audio: {e}")
            return None

    def procesador_entropico(self, señal, nombre_grafico="analisis_espectral_depresion.png"):
        """
        Procesador Entrópico: Analiza la señal, identifica la entropía (rigidez/baja complejidad)
        y genera una \'contraonda espejo\' de alta entropía funcional controlada.
        """
        print("\n[2. PROCESADOR] Analizando la entropía de la señal...")
        
        # Aplica la Transformada Rápida de Fourier (FFT) para pasar al dominio de la frecuencia
        espectro = rfft(señal)
        frecuencias = np.fft.rfftfreq(len(señal), 1 / self.tasa_muestreo)
        
        # Crea el espectro de la contraonda (inicialmente vacío)
        espectro_contraonda = np.zeros_like(espectro)

        # Define las máscaras booleanas para las bandas de frecuencia
        mascara_activacion = (frecuencias >= BANDA_ACTIVACION[0]) & (frecuencias <= BANDA_ACTIVACION[1])
        
        print(f"Creando contraonda... Acentuando la banda de activación ({BANDA_ACTIVACION[0]}-{BANDA_ACTIVACION[1]} Hz).")
        
        # Copia y amplifica la energía de la banda de activación de la señal original a la contraonda
        # Esto hace que la contraonda "resuene" con la activación ya presente (aunque sea mínima)
        espectro_contraonda[mascara_activacion] = espectro[mascara_activacion] * 5 # Mayor amplificación
        
        # Añadir un tono puro y muy audible (ej. 440 Hz - La 4) para asegurar la audibilidad
        # Esto asegura que la contraonda sea siempre audible y clara, independientemente de la señal de entrada
        freq_tono_audible = 440 # Hz
        idx_tono_audible = np.argmin(np.abs(frecuencias - freq_tono_audible))
        # Asegurarse de que el tono se añada con una amplitud considerable
        espectro_contraonda[idx_tono_audible] += np.max(np.abs(espectro)) * 2.0 # Aumentar amplitud del tono

        # Visualiza los espectros para el análisis
        self.visualizar_espectros(frecuencias, espectro, espectro_contraonda, nombre_grafico)
        
        print("Generando la señal de la contraonda desde el espectro modificado...")
        # Aplica la Transformada Inversa para volver al dominio del tiempo
        contraonda = irfft(espectro_contraonda, n=len(señal))
        
        return contraonda

    def decoder(self, señal, nombre_archivo_wav):
        """
        Decodificador: Convierte la señal procesada del campo N de vuelta
        a un formato audible y lo guarda como un archivo .wav.
        """
        print(f"\n[3. DECODER] Guardando la señal procesada en \'{nombre_archivo_wav}\'...")
        
        # Desnormaliza la señal para que tenga un volumen adecuado
        señal_normalizada = señal / np.max(np.abs(señal)) if np.max(np.abs(señal)) > 0 else señal
        amplitud_maxima = np.iinfo(np.int16).max
        señal_int16 = (señal_normalizada * amplitud_maxima).astype(np.int16)
        
        # Escribe el archivo .wav
        wav.write(nombre_archivo_wav, self.tasa_muestreo, señal_int16)
        print("Archivo de audio guardado con éxito.")

    def visualizar_espectros(self, freqs, espectro_original, espectro_procesado, nombre_archivo):
        """
        Genera y guarda un gráfico comparando el espectro original y el procesado.
        """
        print("Generando visualización del análisis espectral...")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        # Gráfico del espectro original
        ax1.plot(freqs, np.abs(espectro_original))
        ax1.set_title("Espectro de la Señal Original (Entrada)")
        ax1.set_ylabel("Amplitud")
        ax1.axvspan(BANDA_DEPRESION[0], BANDA_DEPRESION[1], color='blue', alpha=0.2, label=f'Banda Depresión ({BANDA_DEPRESION[0]}-{BANDA_DEPRESION[1]} Hz)')
        ax1.axvspan(BANDA_ACTIVACION[0], BANDA_ACTIVACION[1], color='orange', alpha=0.3, label=f'Banda Activación ({BANDA_ACTIVACION[0]}-{BANDA_ACTIVACION[1]} Hz)')
        ax1.legend()
        ax1.grid(True, alpha=0.5)

        # Gráfico del espectro de la contraonda
        ax2.plot(freqs, np.abs(espectro_procesado))
        ax2.set_title("Espectro de la Contraonda Espejo (Salida)")
        ax2.set_xlabel("Frecuencia (Hz)")
        ax2.set_ylabel("Amplitud")
        ax2.axvspan(BANDA_ACTIVACION[0], BANDA_ACTIVACION[1], color='orange', alpha=0.3, label=f'Energía Concentrada en Activación')
        ax2.legend()
        ax2.grid(True, alpha=0.5)
        
        plt.xlim(0, 500) # Limita la vista a las frecuencias más relevantes para EEG/Audio bajo
        plt.tight_layout()
        plt.savefig(nombre_archivo)
        print(f"Gráfico de análisis guardado como \'{nombre_archivo}\'.")
        plt.close()

# --- EJECUCIÓN DEL LABORATORIO ---
if __name__ == "__main__":
    
    # --- CONFIGURACIÓN ---
    # Cambia este nombre por el del archivo .wav que quieres procesar.
    # Debe estar en la misma carpeta que este script.
    nombre_archivo_entrada = "1_entrada_simulada_depresion.wav" 
    nombre_archivo_salida = "contraonda_generada_depresion.wav"
    
    # 1. Crear una instancia del laboratorio
    lab = LaboratorioN()
    
    # 2. ENCODER: Cargar la señal
    señal_original = lab.encoder(nombre_archivo_entrada)
    
    if señal_original is not None:
        # 3. PROCESADOR: Generar la contraonda
        contraonda = lab.procesador_entropico(señal_original)
        
        # 4. DECODER: Guardar la nueva señal
        lab.decoder(contraonda, nombre_archivo_salida)
        
        print(f"\n✅ Proceso completado. Escucha \'{nombre_archivo_salida}\' y revisa \'analisis_espectral_depresion.png\'.")



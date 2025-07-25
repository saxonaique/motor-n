import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Añadir el directorio del script al sys.path para imports locales
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from laboratorio_n import LaboratorioN
from guardar_output import guardar_resultados

class LaboratorioNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Laboratorio N - Procesamiento de Señales")
        self.lab = LaboratorioN()
        self.resultados = None

        # --- Layout principal horizontal ---
        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)
        # --- Canvas a la izquierda ---
        self.canvas_size = 400
        self.grid_size = 50
        self.cell_size = self.canvas_size // self.grid_size
        self.animando = False
        self.canvas = tk.Canvas(self.frame_principal, width=self.canvas_size, height=self.canvas_size, bg='black')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        # --- Panel de métricas y gráfico a la derecha ---
        self.frame_metricas = tk.Frame(self.frame_principal)
        self.frame_metricas.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # --- Box gráfico de métricas y métricas a la derecha ---
        import matplotlib
        matplotlib.use('Agg')  # Evita conflictos de backend
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.pyplot as plt
        self.metricas_hist = {'entropia': [], 'varianza': [], 'maximo': [], 'steps': []}
        # El gráfico y el label ahora están en frame_metricas (a la derecha)
        self.frame_grafico = tk.Frame(self.frame_metricas)
        self.frame_grafico.pack(pady=5)
        self.fig, self.ax = plt.subplots(figsize=(4,2), dpi=100)
        self.ax.set_title('Evolución de Métricas')
        self.ax.set_xlabel('Paso')
        self.ax.set_ylabel('Valor')
        self.linea_ent, = self.ax.plot([], [], label='Entropía', color='orange')
        self.linea_var, = self.ax.plot([], [], label='Varianza', color='blue')
        self.linea_max, = self.ax.plot([], [], label='Máximo', color='green')
        self.ax.legend()
        self.canvas_grafico = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas_grafico.get_tk_widget().pack()
        self.label_metricas = tk.Label(self.frame_metricas, text="", font=("Arial", 12), pady=5)
        self.label_metricas.pack()
        # Box gráfico solo para la varianza
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.pyplot as plt
        self.fig_var, self.ax_var = plt.subplots(figsize=(4,1.2), dpi=100)
        self.ax_var.set_title('Evolución de Varianza')
        self.ax_var.set_xlabel('Paso')
        self.ax_var.set_ylabel('Var')
        self.linea_varianza, = self.ax_var.plot([], [], color='#0077ff', label='Varianza')
        self.ax_var.legend()
        self.canvas_varianza = FigureCanvasTkAgg(self.fig_var, master=self.frame_metricas)
        self.canvas_varianza.get_tk_widget().pack(pady=(5,10))


        frame_controles = tk.Frame(root)
        frame_controles.pack(pady=5)
        self.btn_play = tk.Button(frame_controles, text="▶️ Iniciar", command=self.toggle_animacion, bg="#ff6600", fg="white")
        self.btn_play.pack(side=tk.LEFT, padx=5)
        self.btn_reset = tk.Button(frame_controles, text="🔄 Reset", command=self.resetear_campo, bg="#cc0000", fg="white")
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        self.btn_inyectar = tk.Button(frame_controles, text="💥 Inyectar Ansiedad", command=self.inyectar_patron_ansiedad, bg="#0a0", fg="white")
        self.btn_inyectar.pack(side=tk.LEFT, padx=5)
        self.btn_exportar = tk.Button(frame_controles, text="⬇️ Exportar JSON", command=self.exportar_json, bg="#0080ff", fg="white")
        self.btn_exportar.pack(side=tk.LEFT, padx=5)
        self.btn_importar = tk.Button(frame_controles, text="⬆️ Importar JSON", command=self.importar_json, bg="#ffbb00", fg="black")
        self.btn_importar.pack(side=tk.LEFT, padx=5)

        # Widgets principales
        self.label = tk.Label(root, text="Selecciona un archivo .wav para analizar:")
        self.label.pack(pady=10)

        self.archivo_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.archivo_var, width=50)
        self.entry.pack(padx=5)

        self.boton_examinar = tk.Button(root, text="Examinar", command=self.seleccionar_archivo)
        self.boton_examinar.pack(pady=5)

        self.boton_analizar = tk.Button(root, text="Analizar", command=self.analizar)
        self.boton_analizar.pack(pady=10)

        self.texto_resultado = tk.Text(root, height=10, width=60, state='disabled')
        self.texto_resultado.pack(pady=10)



        self.dibujar_campo()

    def dibujar_campo(self):
        self.canvas.delete("all")
        campo = self.lab.get_campo()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                valor = campo[i, j]
                color = self.valor_a_color(valor)
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#222")
        self.actualizar_metricas()

    def valor_a_color(self, valor):
        # Mapea el valor a un color tipo heatmap
        from matplotlib import cm
        import matplotlib.colors as mcolors
        norm = mcolors.Normalize(vmin=0, vmax=1)
        rgba = cm.inferno(norm(valor))
        r, g, b, _ = [int(x*255) for x in rgba]
        return f'#{r:02x}{g:02x}{b:02x}'

    def ciclo_animacion(self):
        if not self.animando:
            return
        self.lab.evolucionar_campo()
        self.dibujar_campo()
        self.root.after(60, self.ciclo_animacion)

    def toggle_animacion(self):
        if self.animando:
            self.animando = False
            self.btn_play.config(text="▶️ Iniciar", bg="#ff6600")
        else:
            self.animando = True
            self.btn_play.config(text="⏸️ Pausar", bg="#ff3300")
            self.ciclo_animacion()

    def resetear_campo(self):
        self.animando = False
        self.btn_play.config(text="▶️ Iniciar", bg="#ff6600")
        self.lab.resetear_campo()
        self.dibujar_campo()

    def inyectar_patron_ansiedad(self):
        if hasattr(self.lab, 'inyectar_patron_ansiedad'):
            self.lab.inyectar_patron_ansiedad()
            self.dibujar_campo()
        else:
            from tkinter import messagebox
            messagebox.showerror("No implementado", "El método inyectar_patron_ansiedad no está implementado en LaboratorioN.")

    def exportar_json(self):
        from tkinter import filedialog, messagebox
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if ruta:
            try:
                self.lab.exportar_estado(ruta)
                messagebox.showinfo("Exportación exitosa", f"Estado exportado a {ruta}")
            except Exception as e:
                messagebox.showerror("Error al exportar", str(e))

    def importar_json(self):
        from tkinter import filedialog, messagebox
        ruta = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if ruta:
            try:
                self.lab.importar_estado(ruta)
                self.dibujar_campo()
                messagebox.showinfo("Importación exitosa", f"Estado importado de {ruta}")
            except Exception as e:
                messagebox.showerror("Error al importar", str(e))

    def actualizar_metricas(self):
        metricas = self.lab.calcular_metricas() if hasattr(self.lab, 'calcular_metricas') else None
        if metricas:
            texto = f"Entropía: {metricas['entropia']:.3f}    Máximo: {metricas['maximo']:.3f}"
            # Actualiza historial de métricas
            paso = len(self.metricas_hist['steps'])
            self.metricas_hist['entropia'].append(metricas['entropia'])
            self.metricas_hist['varianza'].append(metricas['varianza'])
            self.metricas_hist['maximo'].append(metricas['maximo'])
            self.metricas_hist['steps'].append(paso)
            self.actualizar_grafico_metricas()
            self.actualizar_grafico_varianza()
        else:
            texto = ""
        self.label_metricas.config(text=texto)

    def actualizar_grafico_varianza(self):
        pasos = self.metricas_hist['steps']
        self.linea_varianza.set_data(pasos, self.metricas_hist['varianza'])
        self.ax_var.relim()
        self.ax_var.autoscale_view()
        self.canvas_varianza.draw()

    def actualizar_grafico_metricas(self):
        pasos = self.metricas_hist['steps']
        self.linea_ent.set_data(pasos, self.metricas_hist['entropia'])
        self.linea_var.set_data(pasos, self.metricas_hist['varianza'])
        self.linea_max.set_data(pasos, self.metricas_hist['maximo'])
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas_grafico.draw()

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos WAV, PNG o JSON", "*.wav *.png *.json"), ("Todos los archivos", "*.*")])
        if archivo:
            self.archivo_var.set(archivo)


    def analizar(self):
        archivo = self.archivo_var.get()
        self.texto_resultado.config(state='normal')
        self.texto_resultado.delete('1.0', tk.END)
        try:
            if archivo and os.path.isfile(archivo):
                print(f"[1. ENCODER] Cargando señal desde '{archivo}'...")
                resultado = self.lab.encoder(archivo)
                # Adaptar resultado al campo si es posible
                import numpy as np
                arr = np.array(resultado)
                if arr.size >= self.grid_size * self.grid_size:
                    arr = arr[:self.grid_size * self.grid_size]
                else:
                    arr = np.pad(arr, (0, self.grid_size * self.grid_size - arr.size), mode='constant')
                arr = arr.reshape((self.grid_size, self.grid_size))
                arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)  # normaliza a [0,1]
                self.lab.campo = arr
                self.dibujar_campo()
                self.resultados = resultado
                # Mostrar tipo de archivo procesado
                if archivo.lower().endswith('.wav'):
                    self.texto_resultado.insert(tk.END, f"[Archivo .wav] Resultado del encoder:\n{resultado}")
                elif archivo.lower().endswith('.png'):
                    self.texto_resultado.insert(tk.END, f"[Archivo .png] Resultado del encoder (imagen espectral):\n{resultado}")
                else:
                    self.texto_resultado.insert(tk.END, f"[Archivo] Resultado del encoder:\n{resultado}")
            else:
                # Procesar el campo actual del autómata
                print("[2. PROCESADOR] Analizando el campo actual del autómata...")
                campo = self.lab.get_campo().flatten()
                resultado = self.lab.procesador_entropico(campo)
                self.resultados = resultado
                self.texto_resultado.insert(tk.END, "[Campo Motor-N] Resultado del procesador_entropico (contraonda generada):\n")
                self.texto_resultado.insert(tk.END, str(resultado))
            self.texto_resultado.config(state='disabled')
            self.boton_guardar.config(state='normal')
        except Exception as e:
            self.texto_resultado.insert(tk.END, f"Error en el procesamiento: {e}")
            self.texto_resultado.config(state='disabled')
            messagebox.showerror("Error en el procesamiento", str(e))


    def guardar(self):
        if self.resultados is not None:
            guardar_resultados(self.resultados)
            messagebox.showinfo("Guardado", "Resultados guardados exitosamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LaboratorioNApp(root)
    root.mainloop()

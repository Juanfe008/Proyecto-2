import tkinter as tk
from tkinter import ttk

class InterfazGrafica:
    def __init__(self, automata):
        """
        Inicializa la interfaz gráfica para la simulación del autómata celular.
        """
        self.automata = automata
        self.root = tk.Tk()  # Crea la ventana principal
        self.root.title("Simulación de Autómata")  # Título de la ventana
        
        # Configura el marco principal
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Crea el canvas para dibujar la cuadrícula
        self.canvas = tk.Canvas(main_frame, width=650, height=650)
        self.canvas.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

        # Diccionario de reglas disponibles
        self.reglas = {
            'Mejora de Infraestructura': self.automata.regla_mejora_infraestructura,
            'Educación y Juventud': self.automata.regla_educacion_juventud,
            'Política de Redistribución': self.automata.regla_redistribucion
        }
        self.regla_seleccionada = tk.StringVar()
        self.regla_seleccionada.set('Mejora de Infraestructura')  # Regla por defecto

        # Menú desplegable para seleccionar la regla
        self.menu_reglas = ttk.OptionMenu(main_frame, self.regla_seleccionada, 'Mejora de Infraestructura', *list(self.reglas.keys()))
        self.menu_reglas.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Botón para iterar la simulación
        self.boton_iterar = ttk.Button(main_frame, text="Iterar", command=self.iterar)
        self.boton_iterar.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Configuración de las columnas y filas para que se expandan correctamente
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def iterar(self):
        """
        Aplica la regla seleccionada a la cuadrícula y la redibuja.
        """
        regla = self.reglas[self.regla_seleccionada.get()]
        self.automata.aplicar_regla_transicion(regla)
        self.dibujar_grid()

    def dibujar_grid(self):
        """
        Dibuja la cuadrícula en el canvas, coloreando cada celda según su estado.
        """
        self.canvas.delete("all")  # Borra todo el contenido del canvas
        for i in range(self.automata.filas):
            for j in range(self.automata.columnas):
                celda = self.automata.grid[i][j]
                color = self.obtener_color(celda)
                # Dibuja un rectángulo para cada celda, con un color según su estado
                self.canvas.create_rectangle(j * 15, i * 15, (j + 1) * 15, (i + 1) * 15, fill=color)

    def obtener_color(self, celda):
        """
        Devuelve un color basado en el estado socioeconómico de la celda.
        """
        if (celda.estado == 'bajo'):
            return 'red'
        elif (celda.estado == 'medio'):
            return 'yellow'
        else:
            return 'dark green'

    def ejecutar(self):
        """
        Ejecuta el bucle principal de la interfaz gráfica.
        """
        self.dibujar_grid()  # Dibuja la cuadrícula inicial
        self.root.mainloop()  # Inicia el bucle de eventos de Tkinter
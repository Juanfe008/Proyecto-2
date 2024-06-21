from celda import Celda
import numpy as np

class AutomataCelular:
    def __init__(self, filas, columnas):
        """
        Inicializa el autómata celular con una cuadrícula de tamaño filas x columnas.
        Cada celda es una instancia de la clase Celda, con atributos generados aleatoriamente.
        """
        self.filas = filas
        self.columnas = columnas
        self.grid = np.array([[Celda(
            np.random.randint(10000, 70000),  # Ingreso entre 10000 y 70000
            np.random.randint(1, 100),  # Densidad entre 1 y 100
            self.generar_servicios(),  # Servicios generados aleatoriamente
            np.random.randint(20, 80),  # Edad promedio entre 20 y 80
            np.random.choice(['primaria', 'secundaria', 'universitaria'])  # Nivel educativo aleatorio
        ) for _ in range(columnas)] for _ in range(filas)])
    
    def generar_servicios(self):
        """
        Genera una lista de servicios aleatorios para una celda.
        Los servicios posibles son 'escuela', 'hospital' y 'tienda'.
        """
        servicios_posibles = ['escuela', 'hospital', 'tienda']
        numero_servicios = np.random.randint(0, 4)  # Número aleatorio de servicios entre 0 y 3
        if numero_servicios == 0:
            return []
        return np.random.choice(servicios_posibles, numero_servicios, replace=False).tolist()

    def aplicar_regla_transicion(self, regla):
        """
        Aplica una regla de transición a todas las celdas de la cuadrícula.
        """
        nueva_grid = np.empty((self.filas, self.columnas), dtype=object)
        for i in range(self.filas):
            for j in range(self.columnas):
                nueva_grid[i, j] = regla(i, j)
        self.grid = nueva_grid

    def regla_mejora_infraestructura(self, x, y):
        """
        Regla de transición que mejora la infraestructura basada en los servicios de los vecinos.
        """
        celda_actual = self.grid[x][y]
        vecinos = self.obtener_vecinos(x, y)

        # Contar los servicios en los vecinos
        escuelas_vecinos = sum(vecino.servicios.count('escuela') for vecino in vecinos)
        hospitales_vecinos = sum(vecino.servicios.count('hospital') for vecino in vecinos)
        tiendas_vecinos = sum(vecino.servicios.count('tienda') for vecino in vecinos)

        # Pesos para cada tipo de servicio
        peso_escuela = 3
        peso_hospital = 2
        peso_tienda = 1

        # Calcular el impacto total de los servicios
        impacto_servicios = (escuelas_vecinos * peso_escuela +
                             hospitales_vecinos * peso_hospital +
                             tiendas_vecinos * peso_tienda)

        # Ajustar ingreso y densidad según el impacto de los servicios
        if impacto_servicios > 20:
            nueva_ingreso = celda_actual.ingreso * 1.10
            nueva_densidad = celda_actual.densidad * 1.05
        elif impacto_servicios < 10:
            nueva_ingreso = celda_actual.ingreso * 0.90
            nueva_densidad = celda_actual.densidad * 0.95
        else:
            nueva_ingreso = celda_actual.ingreso
            nueva_densidad = celda_actual.densidad

        return Celda(nueva_ingreso, nueva_densidad, celda_actual.servicios, celda_actual.edad_promedio,
                     celda_actual.nivel_educativo)

    def regla_educacion_juventud(self, x, y):
        """
        Regla de transición que ajusta ingreso y edad promedio basado en el nivel educativo de los vecinos.
        """
        celda_actual = self.grid[x][y]
        vecinos = self.obtener_vecinos(x, y)

        # Convertir niveles educativos a valores numéricos y calcular la media
        nivel_educativo_vecinos = np.mean(
            [{'primaria': 1, 'secundaria': 2, 'universitaria': 3}[vecino.nivel_educativo] for vecino in vecinos])

        # Ajustar ingreso y edad promedio basado en el nivel educativo medio de los vecinos
        if nivel_educativo_vecinos > 2:
            nueva_ingreso = celda_actual.ingreso * 1.05
            nueva_edad_promedio = celda_actual.edad_promedio * 0.95
        elif nivel_educativo_vecinos < 1.5:
            nueva_ingreso = celda_actual.ingreso * 0.95
            nueva_edad_promedio = celda_actual.edad_promedio * 1.05
        else:
            nueva_ingreso = celda_actual.ingreso
            nueva_edad_promedio = celda_actual.edad_promedio

        # Determinar el nuevo nivel educativo basado en el nivel medio de los vecinos
        nuevo_nivel_educativo = ['primaria', 'secundaria', 'universitaria'][
            int(round(nivel_educativo_vecinos - 1))]

        return Celda(nueva_ingreso, celda_actual.densidad, celda_actual.servicios, nueva_edad_promedio,
                     nuevo_nivel_educativo)

    def regla_redistribucion(self, x, y):
        """
        Regla de transición que redistribuye ingreso y densidad basado en los promedios de los vecinos.
        """
        celda_actual = self.grid[x][y]
        vecinos = self.obtener_vecinos(x, y)

        # Calcular los promedios de ingreso y densidad de los vecinos
        promedio_ingreso_vecinos = np.mean([vecino.ingreso for vecino in vecinos])
        promedio_densidad_vecinos = np.mean([vecino.densidad for vecino in vecinos])

        # Ajustar ingreso basado en la diferencia con el promedio de los vecinos
        if abs(promedio_ingreso_vecinos - celda_actual.ingreso) > 20000:
            nueva_ingreso = celda_actual.ingreso * 0.90
        else:
            nueva_ingreso = celda_actual.ingreso + (promedio_ingreso_vecinos - celda_actual.ingreso) * 0.2

        # Ajustar densidad basado en la diferencia con el promedio de los vecinos
        if abs(promedio_densidad_vecinos - celda_actual.densidad) > 20:
            nueva_densidad = celda_actual.densidad * 0.90
        else:
            nueva_densidad = celda_actual.densidad + (promedio_densidad_vecinos - celda_actual.densidad) * 0.2

        return Celda(nueva_ingreso, nueva_densidad, celda_actual.servicios, celda_actual.edad_promedio,
                     celda_actual.nivel_educativo)

    def obtener_vecinos(self, x, y):
        """
        Obtiene los vecinos de una celda en la cuadrícula usando la vecindad de Moore.
        """
        vecinos = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if 0 <= x + dx < len(self.grid) and 0 <= y + dy < len(self.grid[0]):
                    vecinos.append(self.grid[x + dx][y + dy])
        return vecinos
class Celda:
    def __init__(self, ingreso, densidad, servicios, edad_promedio, nivel_educativo):
        """
        Inicializa una instancia de Celda con los atributos especificados.
        """
        self.ingreso = ingreso  # Ingreso promedio de la celda
        self.densidad = densidad  # Densidad poblacional de la celda
        self.servicios = list(servicios)  # Lista de servicios disponibles en la celda
        self.edad_promedio = edad_promedio  # Edad promedio de los habitantes de la celda
        self.nivel_educativo = nivel_educativo  # Nivel educativo predominante en la celda
        self.estado = self.definir_estado()  # Estado socioeconómico de la celda

    def definir_estado(self):
        """
        Define el estado socioeconómico de la celda basado en un cálculo de puntaje.
        """
        # Calcula un puntaje basado en los atributos de la celda
        score = (
            self.ingreso / 1000 +  # Contribución del ingreso al puntaje
            self.densidad / 10 +  # Contribución de la densidad al puntaje
            len(self.servicios) * 5 +  # Contribución de la cantidad de servicios al puntaje
            self.edad_promedio / 5 +  # Contribución de la edad promedio al puntaje
            {'primaria': 1, 'secundaria': 2, 'universitaria': 3}[self.nivel_educativo] * 10  # Contribución del nivel educativo al puntaje
        )
        
        # Determina el estado basado en el puntaje calculado
        if score < 40:
            return 'bajo'
        elif 40 <= score < 80:
            return 'medio'
        else:
            return 'alto'
from automata_celular import AutomataCelular
from gui import InterfazGrafica

# Crear una instancia de AutomataCelular con una cuadrícula de 40x40
automata = AutomataCelular(40, 40)

# Crear una instancia de InterfazGrafica pasando el autómata celular creado
interfaz = InterfazGrafica(automata)

# Ejecutar la interfaz gráfica, iniciando el bucle de eventos de Tkinter
interfaz.ejecutar()
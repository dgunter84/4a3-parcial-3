from .cochesBD import CochesBD


class Camiones(CochesBD):
    def __init__(self, marca, color, modelo, velocidad, potencia, asientos):
        super().__init__(marca, color, modelo, velocidad, potencia, asientos)
    self.__eje=eje
    self.__capacidadCarga=capacidadCarga
        
    def acelerar(self):
        self.velocidad=+1
    def frenar(self):
        self.velocidad=-1
    def carga(self,tipo_carga):
        print(f"El tipo de carga es")
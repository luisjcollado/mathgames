from ast import Num
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader

import random
import sys

from matplotlib.colorbar import _ColorbarAxesLocator

logros = {1:(20,.7),2:(40,.7),3:(80,.6),4:(120,.6),5:(200,.5),6:(300,.5),7:(400,.4),8:(500,.4),9:(600,.3),10:(99999999999999,.2)}


class Tablero(BoxLayout):
    nivel = NumericProperty(1)
    mult1 =NumericProperty(0)
    mult2 = NumericProperty(0)
    puntuacion = NumericProperty(0)
    tiempo = NumericProperty(0)

    result1 = NumericProperty(0)
    result2 = NumericProperty(0)
    result3 = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nivel = kwargs["nivel"] if "nivel" in kwargs.keys() else 1
        self.sonido_acierto = SoundLoader.load("./assets/sound9.mp3")
        self.sonido_fallo = SoundLoader.load("./assets/sound94.wav")
        self.velocidad = logros[self.nivel][1]

    def generar_desafio(self):

        resultados = []
        self.mult1,self.mult2 = self._generar_multiplicacion()
        self.correcto = self.mult1*self.mult2
        resultados.append(self.correcto)

        resultados.append((self.mult1+1)*self.mult2)
        resultados.append((self.mult1-1)*+self.mult2)

        random.shuffle(resultados)

        self.result1 = resultados[0]
        self.result2 = resultados[1]
        self.result3 = resultados[2]

        self.reloj = Clock.schedule_interval(self._descontar_tiempo,self.velocidad)


    def comprobar_resultado(self,valor):
        
        if valor == self.correcto:
            self.reloj.cancel()
            #Pintamos fiesta en el widget
            self.sonido_acierto.play()
            self.puntuacion += self.nivel
            self.tiempo -= 50
            if self.tiempo < 0: self.tiempo =0

            if self.puntuacion > logros[self.nivel][0]:
                self.nivel += 1
                self.velocidad = logros[self.nivel][1]

                self.reloj.cancel()
                
            
            self.generar_desafio()

        else: 
            self.sonido_fallo.play()
            self.puntuacion -= 5
            self.tiempo += 50


    def _generar_multiplicacion(self):
        max = self.nivel * 2 if self.nivel<5 else 9
        mult1 = random.randint(2,max)
        mult2 = random.randint(2,9)
        return mult1,mult2

    def _descontar_tiempo(self,dt):
        self.tiempo += 10
        if self.tiempo > 1000: 
            self.reloj.cancel()
            print("final")

            #Mostrar resumen y volver al juego


class MultiApp(App):
    def build(self):
        juego = Tablero()
        juego.nivel = 5
        juego.generar_desafio()
        return juego


if __name__== '__main__':
    MultiApp().run()
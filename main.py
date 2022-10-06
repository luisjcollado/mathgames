from ast import Num
from tokenize import String
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty,StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.audio import SoundLoader

import random
import shelve



logros = {1:(20,.7),2:(40,.7),3:(80,.6),4:(120,.6),5:(200,.5),6:(300,.5),7:(400,.4),8:(500,.4),9:(600,.3),10:(99999999999999,.2)}

class Desafio_matematicas_intro(BoxLayout):
    texto = StringProperty("Estás a punto de iniciar el desafío de matemáticas, "\
            "responde rápidamente para que no te quedes sin tiempo, pero ten cuidado"\
            "porque los fallos descuentan puntos y tiempo.\n\n"\
            "¡¡ A por el record !!")

    texto2 = StringProperty("")
    def __init__(self,app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        records = shelve.open("records.db")
        self.record = int(records['multi']) if 'multi' in records else 0
        self.texto2 = "El record está en {}".format(self.record)
        records.close()


    def iniciar_desafio(self):
        self.app.root.clear_widgets()
        desafio = Tablero(self.app,self.record)
        desafio.generar_desafio()
        self.app.root.add_widget(desafio)


class Tablero(BoxLayout):
    nivel = NumericProperty(1)
    mult1 =NumericProperty(0)
    mult2 = NumericProperty(0)
    puntuacion = NumericProperty(0)
    tiempo = NumericProperty(0)
    record = NumericProperty(0)

    result1 = NumericProperty(0)
    result2 = NumericProperty(0)
    result3 = NumericProperty(0)

    def __init__(self,app,record=0, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.nivel = kwargs["nivel"] if "nivel" in kwargs.keys() else 1
        self.sonido_acierto = SoundLoader.load("./assets/sound9.mp3")
        self.sonido_fallo = SoundLoader.load("./assets/sound94.wav")
        self.velocidad = logros[self.nivel][1]
        self.record = record

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
            ########### PENALIZACION ##################
            self.sonido_fallo.play()
            self.puntuacion -= 5
            if self.puntuacion < 0: self.puntuacion = 0
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
            self.app.cargar_pantalla(Desafio_Matematicas_fin(self.puntuacion,self.record))
          

class Desafio_Matematicas_fin(AnchorLayout):
    resultado=StringProperty()

    def __init__(self,puntuacion=0,record=0, **kwargs):
        super().__init__(**kwargs)

        self.record = record

        if puntuacion > record:
            self.resultado = "[color=10ff10]¡¡ F A N T Á S T I C O!!\n"
            self.resultado += "Conseguiste un nuevo Record:!!\n"
            self.resultado += "[size=60][b]{}[/b][/size][/color]".format(puntuacion)
            db = shelve.open("records.db")
            self.record = puntuacion
            db["multi"]=int(puntuacion)
            db.close()

        else:
            self.resultado= "[color=aa2222]¡¡ F A L L O !!\n"
            self.resultado += "Tu puntuación ha sido: [b]{}[/b]\n".format(puntuacion)
            self.resultado += "El record sigue estando en [b]{}[/b][/color]".format(record)
                

    def cargar_menu(self,app):
        app.cargar_pantalla(MenuPrincipal())

    def cargar_juego(self,app):
        tablero = Tablero(app,self.record)
        tablero.generar_desafio()
        app.cargar_pantalla(tablero)

    
class MenuPrincipal(BoxLayout):
    pass


class MultiApp(App):
    def cargar_desafio_multiplicacion(self):
        self.root.clear_widgets()
        nT = Desafio_matematicas_intro(self)
        self.root.add_widget(nT)

    def cargar_menu(self):
        self.root.clear_widgets()
        self.root.add_widget(MenuPrincipal())

    def cargar_pantalla(self,widget):
        self.root.clear_widgets()
        self.root.add_widget(widget)


 
if __name__== '__main__':
    MultiApp().run()
from tkinter import Frame, Label, Checkbutton, BooleanVar
import time

class MainFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=420, heigh=270)
        self.master =   master

        self.pack()
        time.sleep(1)
        self.value_emergencia = BooleanVar()
        self.create_widgets()

    def fnEnviarEmergencia(self):
        pass

    def create_widgets(self):
        #   Barra de estados
        Label(self, text="Estado", font=(None, 12, 'bold')).place(x=30, y=20)
        #   estado de la barrear

        #   Semaforo
        Label(self, text="Semaforo", font=(None, 10)).place(x=30, y=60)
        Label(self, bg="green", width=3, heigh=1).place(x=150, y=60)
        Label(self, bg="yellow", width=3, heigh=1).place(x=200, y=60)
        Label(self, bg="red", width=3, heigh=1).place(x=250, y=60)

        #   Sensores
        Label(self, text="Sensores", font=(None, 12, 'bold')).place(x=30, y=100)
        Label(self, text="En vias").place(x=30, y=130)
        Label(self, text="sensor 1:").place(x=30, y=150)
        #   Estado del sensor desde arduino
        Label(self, text="sensor 2:").place(x=120, y=150)
        #   Estado del sensor 2 desde el arduino
        Label(self, text="En barrera").place(x=230, y=130)
        Label(self, text="sensor 3:").place(x=230, y=150)

        #   Emergencia
        Checkbutton(self,
                    text    =   "Emergencia",
                    font    =   (None, 10, 'bold'),
                    variable=   self.value_emergencia,
                    onvalue =   1,
                    offvalue=   0,
                    command =   self.fnEnviarEmergencia
                    ).place(x=30, y=190)

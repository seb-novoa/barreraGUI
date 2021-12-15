from tkinter import Frame, Label, Checkbutton, BooleanVar, IntVar, StringVar
import serial
import time
import threading

puerto  =   "/dev/ttyACM0"  # para Windows cambiar a COM*

class MainFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=420, heigh=270)
        self.master =   master
        self.master.protocol('WM_DELETE_WINDOW', self.askQuit)
        self.pack()

        #   Crear un hilo para obtener los datos desde el arduino
        self.hilo1  =   threading.Thread(target=self.getValues, daemon=True)
        self.estados=   threading.Thread(target=self.getEstados, daemon=True)

        #   Comunicacion con el arduino
        self.arduino    =   serial.Serial(puerto, 9600, timeout=1.0)
        time.sleep(1)

        #   Variables de sistema
        self.isRun      =   False
        self.value_estado = StringVar(value = "En linea")


        #   Variables salida
        self.value_emergencia = IntVar()

        #   Variables de entrada
        self.value_rojo     =   IntVar().set(0)
        self.value_amarillo =   IntVar().set(0)
        self.value_verde    =   IntVar().set(0)

        self.hilo1.start()
        self.create_widgets()

    def getEstados(self):
        pass

    def fnEnviarEmergencia(self):
        self.value_rojo     =   self.value_emergencia.get()
        self.value_amarillo =   self.value_emergencia
        self.value_verde    =   self.value_emergencia

        self.fnSemaforo(self.value_emergencia.get())
        if (self.value_emergencia.get()):
            self.value_estado.set("EMERGENCIA")
        else:
            self.value_estado.set("En linea")

    #   Funcion que obtiene los valores desde arduino
    #       label:value
    def getValues(self):
        while self.isRun:
            cad  =   self.arduino.readline().decode('ascii').strip()
            if cad:
                pos = cad.index(":")
                label    =   cad[:pos]
                value    =   cad[pos+1:]

                #    Asignando los valores a su respectiva variables
                if label == 'rojo':
                    self.value_rojo.set(value)
                    print('rojo:' + value)
                if label == 'amarillo':
                    self.value_amarillo.set(value)
                    print('amarillo:' + value)
                if label == 'verde':
                    self.value_verde.set(value)
                    print('verde:' + value)

    #   Funcion de cierre
    def askQuit(self):
        self.isRun  =   False

        self.arduino.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print('***FINALIZANDO...')


    def fnSemaforo(self, emergencia):
        #   Semaforo
        if emergencia:
            Label(self, bg="green", width=3, heigh=1).place(x=150, y=60)
            Label(self, bg="yellow", width=3, heigh=1).place(x=200, y=60)
            Label(self, bg="red", width=3, heigh=1).place(x=250, y=60)
        else:
            Label(self, bg="gray", width=3, heigh=1).place(x=150, y=60)
            Label(self, bg="gray", width=3, heigh=1).place(x=200, y=60)
            Label(self, bg="gray", width=3, heigh=1).place(x=250, y=60)

        
    def create_widgets(self):
        #   Barra de estados
        Label(self, text="Estado", font=(None, 12, 'bold')).place(x=30, y=20)
        Label(self, textvariable = self.value_estado, font=(None, 12, 'bold')).place(x=150, y=20)
        #   estado de la barrear

        #   Semaforo
        Label(self, text="Semaforo", font=(None, 10)).place(x=30, y=60)
        self.fnSemaforo(self.value_emergencia.get())

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

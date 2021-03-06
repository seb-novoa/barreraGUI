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

        #   Comunicacion con el arduino
        self.arduino    =   serial.Serial(puerto, 9600, timeout=1.0)
        time.sleep(1)

        #   Variables de sistema
        self.isRun      =   True
        self.value_estado = StringVar(value = "En linea")


        #   Variables salida
        self.value_emergencia = IntVar()

        #   Variables de entrada
        self.value_rojo     =   IntVar().set(0)
        self.value_amarillo =   IntVar().set(0)
        self.value_verde    =   IntVar().set(0)
        self.value_sensor1  =   IntVar()
        self.value_sensor2  =   IntVar().set(0)
        self.value_sensor3  =   IntVar().set(0)

        self.hilo1.start()
        self.fnIdle()
        self.create_widgets()

    def fnIdle(self):
        print('Barrera a la espera')
        self.arduino.write("verde:1".encode("ascii"))
        self.fnSemaforo((1,0,0))


    def fnEnviarEmergencia(self):
        self.value_rojo     =   self.value_emergencia.get()
        self.value_amarillo =   self.value_emergencia
        self.value_verde    =   self.value_emergencia

        if (self.value_emergencia.get()):
            self.value_estado.set("EMERGENCIA")
            self.arduino.write("emergencia:1".encode("ascii"))
            time.sleep(1.1)
            self.fnSemaforo((1,1,1))
        else:
            self.value_estado.set("En linea")
            self.arduino.write("emergencia:0".encode("ascii"))
            time.sleep(1.1)
            self.fnIdle()

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
                #if label == 'rojo':
                #    self.value_rojo.set(value)
                #    print('rojo:' + value)
                #if label == 'amarillo':
                #    self.value_amarillo.set(value)
                #    print('amarillo:' + value)
                #if label == 'verde':
                #    self.value_verde.set(value)
                #    print('verde:' + value)
                # Sensores
                if label == 'sensor1':
                    self.value_sensor1.set(value)
                    if value == 1 :
                       print('Tren detectado')

    #   Funcion de cierre
    def askQuit(self):
        self.isRun  =   False

        self.arduino.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print('***FINALIZANDO...')


    def fnSemaforo(self, semaforo):
        #   Semaforo
        #   VERDE
        if(semaforo[0]):
            Label(self, bg="green", width=3, heigh=1).place(x=150, y=60)
        else:
            Label(self, bg="gray", width=3, heigh=1).place(x=150, y=60)
        #   AMARILLO
        if(semaforo[1]):
            Label(self, bg="yellow", width=3, heigh=1).place(x=200, y=60)
        else:
            Label(self, bg="gray", width=3, heigh=1).place(x=200, y=60)

        #   ROJO
        if(semaforo[2]):
            Label(self, bg="red", width=3, heigh=1).place(x=250, y=60)
        else:
            Label(self, bg="gray", width=3, heigh=1).place(x=250, y=60)

        
    def create_widgets(self):
        #   Barra de estados
        Label(self, text="Estado", font=(None, 12, 'bold')).place(x=30, y=20)
        Label(self, textvariable = self.value_estado, font=(None, 12, 'bold')).place(x=150, y=20)
        #   estado de la barrear

        #   Semaforo
        Label(self, text="Semaforo", font=(None, 10)).place(x=30, y=60)

        #   Sensores
        Label(self, text="Sensores", font=(None, 12, 'bold')).place(x=30, y=100)
        Label(self, text="En vias").place(x=30, y=130)
        Label(self, text="sensor 1:").place(x=30, y=150)
        Label(self, textvariable=self.value_sensor1).place(x=95, y=150)
        #   Estado del sensor desde arduino
        Label(self, text="sensor 2:").place(x=120, y=150)
        Label(self, text="0",textvariable=self.value_sensor2).place(x=185, y=150)
        #   Estado del sensor 2 desde el arduino
        Label(self, text="En barrera").place(x=230, y=130)
        Label(self, text="sensor 3:").place(x=230, y=150)
        Label(self, text="0",textvariable=self.value_sensor3).place(x=295, y=150)

        #   Emergencia
        Checkbutton(self,
                    text    =   "Emergencia",
                    font    =   (None, 10, 'bold'),
                    variable=   self.value_emergencia,
                    onvalue =   1,
                    offvalue=   0,
                    command =   self.fnEnviarEmergencia
                    ).place(x=30, y=190)

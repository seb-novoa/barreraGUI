from tkinter import Frame, StringVar, Label
import serial
import time
import threading

class MainFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=420, heigh=270)
        self.master = master
        self.master.protocol('WM_DELETE_WINDOW', self.askQuit)
        self.pack()

        self.hilo1 = threading.Thread(target=self.getValues, daemon=True)

        self.arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1.0)
        time.sleep(1)


        self.value_estado = StringVar()

        self.create_widgets()

        self.isRun = True
        self.hilo1.start()

    def askQuit(self):
        self.isRun = False

        self.arduino.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()

        print("adios")

    def getValues(self):
        while self.isRun:
            cad = self.arduino.readline().decode('ascii').strip()
            if cad:
                pos = cad.index(":")
                label = cad[:pos]
                value = cad[pos+1:]

                if label == "verde":
                   self.fnSemaforo((1,0,0))
                   self.value_estado.set("En espera")
                if label == "amarillo":
                    self.fnSemaforo((0,1,0))
                    self.value_estado.set("Precaucion")
                if label == "rojo":
                    self.fnSemaforo((0,0,1))
                    self.value_estado.set("Alto")
                if label == "emergencia":
                    self.fnSemaforo((1,1,1))
                    self.value_estado.set("Paro emergencia")


    def fnSemaforo(self, semaforo):
        #Verde
        if(semaforo[0]):
            Label(self, bg="green", width = 12, heigh = 4).place(x=30, y=20)
        else:
            Label(self, bg="gray", width = 12, heigh = 4).place(x=30, y=20)
        #Amarillo
        if(semaforo[1]):
            Label(self, bg="yellow", width = 12, heigh = 4).place(x=130, y=20)
        else:
            Label(self, bg="gray", width = 12, heigh = 4).place(x=130, y=20)
        if semaforo[2]:
            Label(self, bg="red", width = 12, heigh = 4).place(x=230, y=20)
        else:
            Label(self, bg="gray", width = 12, heigh = 4).place(x=230, y=20)



    def create_widgets(self):
        #Barra de estados
        Label(self,
              text = "Estado",
              font = (None, 12, 'bold')
              ).place(x=30, y=100)
        Label(self,
              textvariable = self.value_estado,
              font = (None, 12, 'bold')
              ).place(x=150, y=100)

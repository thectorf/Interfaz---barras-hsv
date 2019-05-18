from tkinter import *
import cv2, threading
from PIL import ImageTk, Image
from time import sleep
from tkinter import filedialog as FileDialog
import numpy as np
import math

start = False
ctrl = 0

class HiloCamara():
    def __init__(self, video_source):
        #threading.Thread.__init__(self, daemon = True)
        #threading.Thread.name="Hilo camara"
        #threading.Thread.target=HiloCamara.get_frame
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError("Error inesperado!")
        #self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        #self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #print(self.width)
        #print(self.height)
    def obtenerFotograma(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return (ret, None)
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

class Iniciar:

    def __init__(self):
        #global start
        self.camara = 0
        self.root = Tk()
        self.root.title("Panel de calibración")
        #self.root.resizable(width=False, height=False)
        self.root.geometry("900x600")
        #FRAME DE CONTROLES
        frameLeft = Frame()
        frameLeft.pack(side = "left")
        frameLeft.config(width="260", height="480", padx=10)
        #LABEL FRAME PANEL DE ENCENDIDO
        group1 = LabelFrame(frameLeft, text="Panel de Encendido/Apagado")
        group1.pack(ipady = 2, pady=10)
        btnEncender = Button(group1, text="Encender", command=self.encender)
        btnEncender.grid(row = 0, column = 0, padx=5)
        btnStart = Button(group1, text="Start", command=self.iniciar)
        btnStart.grid(row = 0, column = 1)
        btnApagar = Button(group1, text="Apagar", command=self.apagar)
        btnApagar.grid(row = 0, column = 2, padx=5)
        #LABEL FRAME PANEL CONTROL HSV
        group2 = LabelFrame(frameLeft, text="CONTROL HSV")
        group2.pack()
        #labels y scales
        lb1 = Label(group2, text= 'HUE MIN:     ', justify = "left")
        lb1.grid(row = 0, column = 0)
        lb2 = Label(group2, text= 'HUE MAX:     ', justify = "left")
        lb2.grid(row = 1, column = 0)
        lb3 = Label(group2, text= 'SAT MIN:     ', justify = "left")
        lb3.grid(row = 2, column = 0)
        lb4 = Label(group2, text= 'SAT MAX:     ', justify = "left")
        lb4.grid(row = 3, column = 0)
        lb5 = Label(group2, text= 'VAL MIN:     ', justify = "left")
        lb5.grid(row = 4, column = 0)
        lb6 = Label(group2, text= 'VAL MAX:     ', justify = "left")
        lb6.grid(row = 5, column = 0, pady=5)

        btnG = Button(group2, text="Guardar", command=self.guardar)
        btnG.grid(row = 6, column = 0)
        self.hmin = Scale(group2, from_=0, to=255, orient=HORIZONTAL)
        self.hmin.grid(row = 0, column = 1)
        self.hmax = Scale(group2, from_=0, to=255, orient=HORIZONTAL)
        self.hmax.grid(row = 1, column = 1)
        self.smin = Scale(group2, from_=0, to=255, orient=HORIZONTAL)
        self.smin.grid(row = 2, column = 1)
        self.smax = Scale(group2, from_=0, to=255, orient=HORIZONTAL)
        self.smax.grid(row = 3, column = 1)
        self.vmin = Scale(group2, from_=0, to=255, orient=HORIZONTAL)
        self.vmin.grid(row = 4, column = 1)
        self.vmax = Scale(group2, from_=0, to=255, orient=HORIZONTAL)
        self.vmax.grid(row = 5, column = 1)
        btnA = Button(group2, text="Abrir", command=self.abrir)
        btnA.grid(row = 6, column = 1, pady=5)

        #FRAME COORDENADAS
        group3 = LabelFrame(frameLeft, text="COORDENADAS Y MEDIDAS")
        group3.pack(pady=10)
        self.varx = StringVar()
        self.varx.set("X: 0")
        self.vary = StringVar()
        self.vary.set("Y: 0")
        self.vars = StringVar()
        self.vars.set("S: 0")
        self.varw = StringVar()
        self.varw.set("W: 0")
        self.varh = StringVar()
        self.varh.set("H: 0")
        Label(group3, textvar= self.varx).grid(row=0, column = 0, padx=5)
        Label(group3, textvar= self.vary).grid(row=0, column = 1, padx=10)
        Label(group3, textvar= self.vars).grid(row=0, column = 2, padx=10)
        Label(group3, textvar= self.varw).grid(row=1, column = 0, padx=5)
        Label(group3, textvar= self.varh).grid(row=1, column = 1, padx=10)

        #FRAME DEL CANVAS
        frameRight = Frame()
        frameRight.pack(side = "right")
        frameRight.config(bg="black", width="640", height="480")
        self.canvas = Canvas(frameRight, width = 640, height = 480, bg = "green")
        self.canvas.pack()
        self.imageDefault = ImageTk.PhotoImage(file='img/default.jpg')
        self.canvas.create_image(0, 0, anchor = NW,  image=self.imageDefault)


        self.root.mainloop()

    def guardar(self):
        fichero = FileDialog.asksaveasfile(title = "Guardar valores", mode = 'w', defaultextension = ".txt", filetype = (("Archivo de texto", "*.txt"),))
        if fichero is not None:
            fichero = open(fichero.name, "w")
            fichero.write(
            "Hue Min:{}\nHue Max:{}\nSat Min:{}\nSat Max:{}\nVal Min:{}\nVal Max:{}".
            format(self.hmin.get(), self.hmax.get(), self.smin.get(), self.smax.get(), self.vmin.get(), self.vmax.get()))
            fichero.close()

    def abrir(self):
        lista = []
        fichero = FileDialog.askopenfilename(title = "Abrir valores", initialdir = '.', filetype = (("Archivo de texto", "*.txt"),))
        if fichero is not '':
            fichero = open(fichero, "r")
            for linea in fichero:
                lista.append("".join([x for x in linea if x.isdigit()]))
            self.hmin.set(lista[0])
            self.hmax.set(lista[1])
            self.smin.set(lista[2])
            self.smax.set(lista[3])
            self.vmin.set(lista[4])
            self.vmax.set(lista[5])
            fichero.close()

    def encender(self):
        global start, ctrl
        self.start = start
        if self.start is False:
            self.cap = HiloCamara(1)
            self.start = True
            start = True
            self.iniciar = False
            if ctrl == 0:
                self.actualizar()

    def iniciar(self):
        self.iniciar = True

    def apagar(self):
        global start, ctrl
        self.start = start
        if self.start:
            self.start = False
            self.cap.cap.release()
            start = False
            ctrl = 1
            self.iniciar = False
            self.reiniciarValores()

    def reiniciarValores(self):
        self.varx.set("X: 0")
        self.vary.set("Y: 0")
        self.varw.set("W: 0")
        self.varh.set("H: 0")
        self.vars.set("S: 0")

    def actualizar(self):
        if self.start:
            ret, frame = self.cap.obtenerFotograma()
            if ret:
                imgTemp = cv2.flip(frame, 1)
                hsv = cv2.cvtColor(imgTemp, cv2.COLOR_BGR2HSV)
                lower = np.array([self.hmin.get(), self.smin.get(), self.vmin.get()])
                upper = np.array([self.hmax.get(), self.smax.get(), self.vmax.get()])
                mask = cv2.inRange(hsv, lower, upper)
                # inicio filtros
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                mask = cv2.dilate(mask, kernel, iterations = 4)
                # fin filtros
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(mask))
                self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

                if self.iniciar:
                    contorno, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for c in contorno:
                        area = cv2.contourArea(c)
                        if area > 200 and area < 100000:
                            cv2.drawContours(mask, contorno, -1, (0, 0, 255), 3, cv2.LINE_AA)
                            (x, y, w, h) = cv2.boundingRect(c)
                            x1 = x + (w/2)
                            y1 = y + (h/2)
                            x2 = x1-320
                            y2 = 480-y1
                            self.varx.set("X: {0:.2f}".format(x2))
                            self.vary.set("Y: {0:.2f}".format(y2))
                            self.varw.set("W: {0:.2f}".format(w))
                            self.varh.set("H: {0:.2f}".format(h))
                            angulo = 0
                            if y2 is not 0:
                                t = math.atan(x2/y2)
                                t = math.degrees(t)
                                self.vars.set("S: {0:.2f}".format(t))
                            else:
                                self.vars.set("S: {}".format(t))
        else:
            self.imageDefault = ImageTk.PhotoImage(file='img/default.jpg')
            self.canvas.create_image(0, 0, anchor = NW,  image=self.imageDefault)
        self.root.after(15, self.actualizar)

Iniciar()

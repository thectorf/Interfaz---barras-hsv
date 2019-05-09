from tkinter import *
from PIL import ImageTk, Image
import cv2, threading
import numpy as np
from io import open
from tkinter import messagebox as MessageBox


start = False
stop = False
imgObject = None
imageDefault = None
hmax = 0
hmin = 0
vmax = 0
vmin = 0
smax = 0
smin = 0

class HiloCapturar(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon = True, target = HiloCapturar.run)
        threading.Thread.name="hilo camara"
        self.cap = None
        global stop
        global imgObject
        global imageDefault
        global hmax, hmin, vmax, vmin, smax, smin, start

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            imgTemp = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(imgTemp, cv2.COLOR_BGR2HSV)
            lower = np.array([hmin.get(), smin.get(), vmin.get()])
            upper = np.array([hmax.get(), smax.get(), vmax.get()])
            #lower = np.array([0, 0, 190])
            #upper = np.array([100, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)
            imgTemp = Image.fromarray(mask)
            imgObject = ImageTk.PhotoImage(imgTemp)
            canvas.itemconfigure(canvasImage, image = imgObject)
            if start:
                contorno, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in contorno:
                    area = cv2.contourArea(c)
                    if area > 200 and area < 100000:
                        cv2.drawContours(mask, contorno, -1, (0, 0, 255), 3, cv2.LINE_AA)
                        (x, y, w, h) = cv2.boundingRect(c)
                        var1.set("X: {}     Y: {}".format(x, y))
                        var2.set("W: {}     H: {}".format(w, h))
                        var3.set("       S: {}".format(x+y))
            #cv2.waitKey(1)
            if stop:
                self.cap.release()
                cv2.destroyAllWindows()
                self.imageDefault = ImageTk.PhotoImage(file = 'img/default.jpg')
                canvas.itemconfigure(canvasImage, image = imageDefault)
                var1.set("X: 0        Y: 0")
                var2.set("W: 0        H: 0")
                var3.set("        S: 0")
                break

def encender():
    global stop
    stop = False
    camara = HiloCapturar()
    camara.start()

def apagar():
    global stop, start
    stop = True
    start = False

def starts():
    global start
    start = True

def guardar():
    global hmax, hmin, vmax, vmin, smax, smin, start
    fichero = open('valores.txt', "w+")
    fichero.write(
    "Hue Min:{}\nHue Max:{}\nSat Min:{}\nSat Max:{}\nVal Min:{}\nVal Max:{}".
    format(hmin.get(), hmax.get(), smin.get(), smax.get(), vmin.get(), vmax.get()))
    fichero.close()
    MessageBox.showinfo("Guardar", "Se guardaron los valores")

def abrir():
    lista = []
    global hmax, hmin, vmax, vmin, smax, smin, start
    fichero = open('valores.txt', "r")
    #lectura = fichero.read()
    #lectura = lectura.split('\n')
    for linea in fichero:
        lista.append("".join([x for x in linea if x.isdigit()]))
    hmin.set(lista[0])
    hmax.set(lista[1])
    smin.set(lista[2])
    smax.set(lista[3])
    vmin.set(lista[4])
    vmax.set(lista[5])
    fichero.close()
    MessageBox.showinfo("Abrir", "Se cargaron los valores")
root = Tk()
root.title("PDI")
root.resizable(width=False, height=False)
root.geometry("900x600")
#FRAME DE CONTROLES
frameLeft = Frame()
frameLeft.pack(side = "left")
frameLeft.config(width="560", height="200")
#LABEL FRAME PANEL DE ENCENDIDO
group1 = LabelFrame(frameLeft, text="Panel de Encendido/Apagado", padx=10, pady=10)
group1.pack(padx=5, pady=10)
btnEncender = Button(group1, text="Encender", command=encender)
btnEncender.pack(side='left')
btnStart = Button(group1, text="Start", command=starts)
btnStart.pack(side='left')
btnApagar = Button(group1, text="Apagar", command=apagar)
btnApagar.pack(side='left')
#LABEL FRAME PANEL CONTROL HSV
group2 = LabelFrame(frameLeft, text="CONTROL HSV", padx=10, pady=10)
group2.pack(padx=5, pady=0)
#FRAME LABELS
labels = LabelFrame(group2)
labels.config(relief="flat")
labels.pack(padx=5, pady=0, side='left')
lb1 = Label(labels, text= 'HUE MIN:     ', justify = "left")
lb1.pack(ipady=10, pady=10)
lb2 = Label(labels, text= 'HUE MAX:     ', justify = "left")
lb2.pack(ipady=10)
lb3 = Label(labels, text= 'SAT MIN:     ', justify = "left")
lb3.pack(ipady=10)
lb4 = Label(labels, text= 'SAT MAX:     ', justify = "left")
lb4.pack(ipady=10)
lb5 = Label(labels, text= 'VAL MIN:     ', justify = "left")
lb5.pack(ipady=10)
lb6 = Label(labels, text= 'VAL MAX:     ', justify = "left")
lb6.pack(ipady=10)
btnG = Button(labels, text="Guardar", command=guardar)
btnG.pack()
#FRAME TRACKS
tracks = LabelFrame(group2)
tracks.config(relief="flat")
tracks.pack(padx=5, pady=10, side='right')
hmin = Scale(tracks, from_=0, to=255, orient=HORIZONTAL)
hmin.pack(ipady=1)
hmax = Scale(tracks, from_=0, to=255, orient=HORIZONTAL)
hmax.pack(ipady=1)
smin = Scale(tracks, from_=0, to=255, orient=HORIZONTAL)
smin.pack(ipady=1)
smax = Scale(tracks, from_=0, to=255, orient=HORIZONTAL)
smax.pack(ipady=1)
vmin = Scale(tracks, from_=0, to=255, orient=HORIZONTAL)
vmin.pack(ipady=1)
vmax = Scale(tracks, from_=0, to=255, orient=HORIZONTAL)
vmax.pack(ipady=1)
btnA = Button(tracks, text="Abrir", command=abrir)
btnA.pack()
#FRAME COORDENADAS
group3 = LabelFrame(frameLeft, text="COORDENADAS Y MEDIDAS", padx=10, pady=10)
group3.pack(padx=5, pady=10)
var1 = StringVar()
var1.set("X: 0        Y: 0")
var2 = StringVar()
var2.set("W: 0        H: 0")
var3 = StringVar()
var3.set("        S: 0")
Label(group3, textvar= var1).grid(row=0)
Label(group3, textvar= var2).grid(row=1)
Label(group3, textvar= var3).grid(row=0, column=1)
#FRAME DEL CANVAS
frameRight = Frame()
frameRight.pack(side = "right")
frameRight.config(bg="green", width="640", height="500")
canvas = Canvas(frameRight, width=640, height=480, bg='black')
canvas.pack()
imageDefault = ImageTk.PhotoImage(file='img/default.jpg')
canvasImage = canvas.create_image(2, 2, anchor=NW,image=imageDefault)

root.mainloop()

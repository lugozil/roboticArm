# importing libraries
import PySimpleGUI as sg
import cv2
import numpy as np 
import math
import data
import utils
import arm 
import threading
from multiprocessing.pool import ThreadPool
import os 
import time 
import customtkinter
import tkinter 
from tkinter import messagebox


pool = ThreadPool(processes=1)

# # viewport for camera
vpc = utils.ViewPort()

# rgb colors for opencv
rgb_black = (0, 0, 0)
rgb_white = (255, 255, 255)
cent =[0,0]
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self): 
        super().__init__()

        self.title("LUBOT")
        self.configure(width=420, height=580)

        #dimensiones de pantalla 
        pantalla_widht = self.winfo_screenwidth()
        pantalla_heigt = self.winfo_screenheight()

        #centro de pantalla 
        pwidth = round( pantalla_widht/2-420/2)
        pheight = round(pantalla_heigt/2-680/2) - 40
        self.geometry(str(420)+"x"+str(680)+"+"+str(pwidth)+"+"+str(pheight))

        # label and button
        self.logo_label = customtkinter.CTkLabel(self, text="Sistema de Clasificación",justify=customtkinter.CENTER ,font=customtkinter.CTkFont(size=25, weight="bold"))
        self.logo_label.place(x=63, y=20)

        self.label_1 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Ingrese cantidad de objetos:",font=customtkinter.CTkFont(size=15))
        self.label_1.place(x=70, y=80)

        validate_entry = lambda text: text.isdecimal()
        self.entry_1 = customtkinter.CTkEntry(self, placeholder_text="Nro de jengas",width=160,height=32,validate="key",validatecommand=(self.register(validate_entry), "%S"))
        self.entry_1.place(x=70, y=120)
        self.campo1 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="*",font=customtkinter.CTkFont(size=12))
        self.campo1.place(x=240, y= 125)

        self.label_2 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Active los colores e indique el destino:",font=customtkinter.CTkFont(size=15))
        self.label_2.place(x=70, y=180)
        
        # Colores y destinos 
        self.fondo_frame = customtkinter.CTkFrame(self,width=260,height=320)
        self.fondo_frame.place(x=70, y=220)

        self.label_3 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Colors",font=customtkinter.CTkFont(size=12),bg_color="gray17")
        self.label_3.place(x=110, y=235)

        self.label_3 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Destinations",font=customtkinter.CTkFont(size=12),bg_color="gray17")
        self.label_3.place(x=230, y=235)

        self.switch_1 = customtkinter.CTkSwitch(self, text="Red", width=10,height=14,switch_width=40,switch_height=20,bg_color="gray17",progress_color="firebrick2")
        self.switch_1.place(x=100, y=280)
        self.segmented_button_1 = customtkinter.CTkSegmentedButton(self, values=["Left", "Right"])
        self.segmented_button_1.place(x=220, y=275)

        self.switch_2 = customtkinter.CTkSwitch(self, text="Green", width=10,height=14,switch_width=40,switch_height=20,bg_color="gray17",progress_color="SpringGreen3")
        self.switch_2.place(x=100, y=330)
        self.segmented_button_2 = customtkinter.CTkSegmentedButton(self, values=["Left", "Right"])
        self.segmented_button_2.place(x=220, y=325)

        self.switch_3 = customtkinter.CTkSwitch(self, text="Blue", width=10,height=14,switch_width=40,switch_height=20,bg_color="gray17",progress_color="RoyalBlue3")
        self.switch_3.place(x=100, y=380)
        self.segmented_button_3 = customtkinter.CTkSegmentedButton(self, values=["Left", "Right"])
        self.segmented_button_3.place(x=220, y=375)

        self.switch_4 = customtkinter.CTkSwitch(self, text="Orange", width=10,height=14,switch_width=40,switch_height=20,bg_color="gray17",progress_color="dark orange")
        self.switch_4.place(x=100, y=430)
        self.segmented_button_4 = customtkinter.CTkSegmentedButton(self, values=["Left", "Right"])
        self.segmented_button_4.place(x=220, y=425)

        self.switch_5 = customtkinter.CTkSwitch(self, text="Brown", width=10,height=14,switch_width=40,switch_height=20,bg_color="gray17",progress_color="saddle brown")
        self.switch_5.place(x=100, y=480)
        self.segmented_button_5 = customtkinter.CTkSegmentedButton(self, values=["Left", "Right"])
        self.segmented_button_5.place(x=220, y=475)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text= "Confirmar")
        self.checkbox_1.place(x=70, y=550)
        self.campo2 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="*",font=customtkinter.CTkFont(size=12))
        self.campo2.place(x=165, y= 550)

        self.button_1 = customtkinter.CTkButton(self, command=self.event_button_start, text="Start",font=customtkinter.CTkFont(size=15))
        self.button_1.place(x=130, y=600)

        self.button_help = customtkinter.CTkButton(self, command=self.event_button_help, text="Help",width=50,height=25,font=customtkinter.CTkFont(size=12))
        self.button_help.place(x=280, y=550)

        self.campo3 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Campos obligatorios (*)",font=customtkinter.CTkFont(size=12))
        self.campo3.place(x=270, y= 650)

        self.campo5 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="*",font=customtkinter.CTkFont(size=12))
        self.campo5.place(x=340, y= 220)


    def event_button_help(self):
        new_window = customtkinter.CTkToplevel(self)
        new_window.configure(width=320, height=380)
        # create textbox
        self.textbox = customtkinter.CTkTextbox(new_window,width=320, height=380,)
        self.textbox.place(x=0,y=0)
        self.textbox.insert("0.0","¿COMO FUNCIONA?\n\n" + "1. Cantidad de Objetos: sirve para indicar la cantidad de jengas que desea clasificar, a pesar de tener   un area de trabajo limitada"+
                            " el robot luego  de  limpiar  la zona, seguira trabajando a medida se coloquen los objetos  en  la  superficie,  hasta  cumplir  con   el   numero indicado.\n\n"+ 
                            "2. Colores y Destinos: para selecionar el color o los  colores  que  se  desean  clasificar, solo basta con    activar la casilla respectiva tanto del color como en  el "+
                            "apartado del destino. Se tiene disponible (RGB) de acuerdo a la composicion de la intensidad del color.  Por  otra  parte, se  puede  indicar  el  destino  como   left(1) o right(2)\n\n"+
                            "3. Confirmar: luego de indicar la cantidad de objetos, los colores y su destino, necesita verificar los datos suministrados marcando dicha casilla.\n\n"+
                            "4. Start: ejecuta el programa.\n\n"+"________________________________________________\n\n"+"INFORMACIÓN DEL ROBOT\n\n"+"- El brazo robotico (LUBOT) posee 5 GDL, posee un movimiento  libre  antropomorfico"+
                            "  para   clasificar    objetos.\n\n"+"- Posee  un  area de  trabajo con un radio  de  21  cm,  con el eje Y positivo. ( vista al frente)\n\n"+"- La estructura "+
                            " fisica  del  robot  esta   formada  con  5  eslabones,  6  servomotores, 1  pinza, 1  tarjeta de control Pololu 12 mini maestro, y su regulador de   5   voltios")

    def event_button_start(self):
        if(self.entry_1.get()!='' and self.checkbox_1.get()==1 and (self.switch_1.get()==1 or self.switch_2.get()==1 or self.switch_3.get()==1) and 
           (self.segmented_button_1.get()!='' or self.segmented_button_2.get()!='' or self.segmented_button_3.get()!='')):
            
                self.cantidad = int(self.entry_1.get())
                self.aux = 1
                arrayColor = []

                self.red = int(self.switch_1.get())
                self.red_destination = self.segmented_button_1.get()
                if(self.red == 1):
                    list_ = ["red",self.red_destination]
                    arrayColor.append(list_)


                self.green = int(self.switch_2.get())
                self.green_destination = self.segmented_button_2.get()
                if(self.green == 1):
                    list_ = ["green",self.green_destination]
                    arrayColor.append(list_)

                self.blue = int(self.switch_3.get())
                self.blue_destination = self.segmented_button_3.get()
                if(self.blue == 1):
                    list_ = ["blue",self.blue_destination]
                    arrayColor.append(list_)              

                self.orange = int(self.switch_4.get())
                self.orange_destination = self.segmented_button_4.get()
                if(self.orange == 1):
                    list_ = ["orange",self.orange_destination]
                    arrayColor.append(list_)

                self.brown = int(self.switch_5.get())
                self.brown_destination = self.segmented_button_5.get()
                if(self.brown == 1):
                    list_ = ["brown",self.brown_destination]
                    arrayColor.append(list_)

                self.array = arrayColor
                resul = self.checkbox_1.get()
                self.quit()
        else: 
            messagebox.showinfo(message="Rellene los campos obligatorios", title="Warning")

def main_layout():
    # define the window layout
    layout = [[sg.Text('Work Area', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')]] 
    return layout

def centroid(count):
    M = cv2.moments(count)
    cx = round(M['m10'] / M['m00'], 2)
    cy = round(M['m01'] / M['m00'], 2)  
    return cx, cy  

def new_corner(corner, num, x, y):
    corner.append(x)
    corner.append(y)
    num = num + 1
    return num 

def diferencial(a,b):
    return ((b/a)*100)-100

def search(color,array2):
    lista = np.array(array2)
    posiciones = np.where(lista == color)
    #posicion = array.index('color')
    posicion = int(posiciones[0])
    destino = array2[posicion][1] # me da el destino
    if(destino=='Left'): destino = 2
    if(destino=='Right'):destino = 1

    return destino

def manage_agent(frame, hsv,array,centro):

    for color in utils.agent.keys(): # busca colores en los angentes
        for colores_activos in array: # 
            if color in colores_activos: # in colores_activos para buscar en toda la lista
                destino = search(color,array) # jenga contiene el color,destino. 1 = right y 2 = left
                is_agent = generate_mask(frame, hsv, color,centro,destino) # enviar color,colores_activos[0][1] u obtener la posicion donde consiguio el color y apartir de este enviarlo 
                if is_agent: 
                    centro = [is_agent.cx,is_agent.cy]

    return 0,centro 

def pixelesextremos(corner1,corner2):
    aux1 = corner1[0]+corner1[1] 
    aux2 = corner2[0]+corner2[1]
    if(aux1>aux2):
        return corner2,corner1 
    else: 
        return corner1,corner2 

def angulos_pulsos(z,min_prev,max_prev,max_new,min_new): 
    return round(((((z-min_prev)/(max_prev-min_prev))*(max_new-min_new))+min_new),2)

def radians2degrees(angle):
    degrees = angle * 180 / math.pi
    return round(degrees, 2)

def calibration(cx2,cy2,orientacion):
    aux = 0 
# MODIFICACIONES PARA AJUSTAR ORIENTACION Y PRECISION DEL ROBOT SEGUN UBICACION FISICA (CALIBRACION)4
#-----------------------------------------------------------------------------------------
# Lado derecho 

    if(cx2 > 0 and orientacion<=90.00): 
        auxorientacion = orientacion
        orientacion = orientacion + 98
        print("entro aqui primero")
        aux = 1
        if(cx2 > 0 and cy2>14 and auxorientacion > 25 and auxorientacion <70): 
            orientacion = orientacion + 4
        elif(cx2>12 and auxorientacion >0 and auxorientacion <25): 
            orientacion = orientacion - 6
            print("entro")

    elif(cx2 > 0 and orientacion>90.00): # cx = cy pq esta invertido 
        auxorientacion = orientacion
        orientacion = orientacion - 82 
        print("entro aqui despues ")
        aux = 1 
        if(cx2 > 12 and orientacion > 0 and orientacion <25): 
            orientacion = orientacion -15 
        elif(cx2>10 and orientacion >25 and orientacion <50):
            orientacion = orientacion -9
            if(cx2>14): orientacion = orientacion - 14
        elif(cx2>0 and cx2<9 and orientacion >50 and orientacion <70): 
            orientacion = orientacion +5
            print("alternativa4")
        elif(cx2>9 and orientacion >50 and orientacion <70): 
            orientacion = orientacion -21
            print("alternativa5")
        elif(cx2>0 and cx2<10 and orientacion > 70 and orientacion < 100): 
            orientacion = orientacion +2
        elif(cx2>10 and orientacion >70 and orientacion <100): 
            orientacion = orientacion - 13
            print("entro aqui ? ")

    # arreglo 
    # if(cx2 < 3 and orientacion<90.00): 
    #     orientacion = orientacion + 100
    #     print("entro aqui primero negativo")
# ----------------------------------------------------------------------------------------
# Lado izquierdo 

    if(cx2 < 0 and orientacion>90.00): # Verificado 
        orientacion = orientacion + 4  # cx = cy pq esta invertido
        aux = 2
        print("entra aqui alternativa 1")
        if(cx2 < -12.5 and orientacion >110.00 and orientacion < 160.00):
            orientacion = orientacion + 12
            aux = 3
        elif(cx2 > -12.5 and orientacion >110.00 and orientacion < 165.00):
            orientacion = orientacion - 7
        elif(cx2 < -12.5 and orientacion > 165 and orientacion < 180):
            orientacion = orientacion + 12
            aux = 3
            if(orientacion > 180): # para que el robot se mueva en la otra orientacion. 
                orientacion = 9
            if(cy2 >14):
                orientacion = orientacion - 7
        elif(cx2<0 and cx2 > -5 and orientacion>110): # acomodar 
            orientacion = orientacion -28
            print("NUEVO")
            
    elif(cx2 < 0 and orientacion < 90.00): # Verificado
        aux = 2
        orientacion = orientacion -3
        if(cx2 < -12.5 and orientacion >20.00 and orientacion < 70.00):
            orientacion = orientacion + 12
            aux = 3
        elif(cx2< -12.5 and orientacion > 0 and orientacion < 20.00):
            orientacion = orientacion + 12 
            aux = 3
        if(cy2 > 14 and cx2 > -12.5 and orientacion >0 and orientacion <20.00):
            orientacion = orientacion -5
            print("entro a esta alternativa ")
 
    return orientacion,aux

def drawAxis(img, p_, q_, color, scale):
  p = list(p_)
  q = list(q_)
 
  ## [visualization1]
  angle = math.atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
  hypotenuse = math.sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
 
  # Here we lengthen the arrow by a factor of scale
  q[0] = p[0] - scale * hypotenuse * math.cos(angle)
  q[1] = p[1] - scale * hypotenuse * math.sin(angle)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
 
  # create the arrow hooks
  p[0] = q[0] + 9 * math.cos(angle + math.pi / 4)
  p[1] = q[1] + 9 * math.sin(angle + math.pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
 
  p[0] = q[0] + 9 * math.cos(angle - math.pi / 4)
  p[1] = q[1] + 9 * math.sin(angle - math.pi / 4)
  cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
  ## [visualization1]

def getOrientation(pts, img):
  ## [pca]
  # Construct a buffer used by the pca analysis
  sz = len(pts)
  data_pts = np.empty((sz, 2), dtype=np.float64)
  for i in range(data_pts.shape[0]):
    data_pts[i,0] = pts[i,0,0]
    data_pts[i,1] = pts[i,0,1]
 
  # Perform PCA analysis
  mean = np.empty((0))
  mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
 
  # Store the center of the object
  cntr = (int(mean[0,0]), int(mean[0,1]))
  ## [pca]
 
  ## [visualization]
  # Draw the principal components
  cv2.circle(img, cntr, 3, (255, 0, 255), 2)
  p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
  p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
  drawAxis(img, cntr, p1, (255, 255, 0), 1)
  drawAxis(img, cntr, p2, (0, 0, 255), 5)
 
  angle = math.atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
  ## [visualization]
 
  # Label with the rotation angle
  label = "  Rotation Angle: " + str(-int(np.rad2deg(angle)) - 90) + " degrees"
  textbox = cv2.rectangle(img, (cntr[0], cntr[1]-25), (cntr[0] + 250, cntr[1] + 10), (255,255,255), -1)
  cv2.putText(img, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
  orientacion = radians2degrees(angle)
  if orientacion < 0: 
    orientacion = orientacion + 180 

  return  orientacion

def draw_half_circle_no_round(image):
    height, width = image.shape[0:2]
    # Ellipse parameters
    radius = 100
    center = (width / 2, height - 25)
    axes = (radius, radius)
    angle = 0
    startAngle = 180
    endAngle = 360
    # When thickness == -1 -> Fill shape
    thickness = -1

    # Draw black half circle
    cv2.ellipse(image, center, axes, angle, startAngle, endAngle, rgb_black, thickness)

    axes = (radius - 10, radius - 10)
    # Draw a bit smaller white half circle
    #cv2.ellipse(image, center, axes, angle, startAngle, endAngle, WHITE, thickness)

def area_trabajo(frame ,min_corner ,max_corner, x2):
    centro = [x2,min_corner[1]]
    medida = centro[0] - min_corner[0]
    axes = (int(medida),int(medida))
    angle, startAngle =0,0;
    endAngle=-180;
    center=(int(centro[0]),int(centro[1]))

    cv2.ellipse(frame, center, axes, angle, startAngle, endAngle, rgb_black,2)
    orige = (int(min_corner[0]),int(min_corner[1]))
    fin = (int(max_corner[0]),int(min_corner[1]))
    cv2.line(frame,orige,fin,rgb_black,2)

def generate_mask(frame, hsv, color,centro,destino):
    mask = cv2.inRange(hsv, np.array(data.HSV_COLORS[color][0]), np.array(data.HSV_COLORS[color][1])) 
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #variables to define the rectangle of viewport
    num_corner = 0
    corner1 = []
    corner2 = []
    lista = []
    newQ5 = 0

    global band, min_prev, max_prev 

    for count in contours:  
        # using functions to get the contour of shapes
        epsilon = 0.01 * cv2.arcLength(count, True)
        approx = cv2.approxPolyDP(count, epsilon, True)
        # get area to work with only visible objects solware y can cat 
        area = cv2.contourArea(count)
        if area > 50:
            # recognize rectangles 
            if len(approx) == 4 and color == 'black': 
                # computes the centroid of shapes 
                cx, cy = centroid(count)
                cv2.circle(frame, (int(cx),int(cy)), 2, rgb_white, 2)
                # rectangles - marks 
                if num_corner == 0: 
                    num_corner = new_corner(corner1, num_corner, cx, cy)
                elif num_corner == 1: 
                    num_corner = new_corner(corner2, num_corner, cx, cy)
                    # draws the region of interest as a rectangle
                    min_prev, max_prev = pixelesextremos(corner1,corner2)
                    cv2.rectangle(frame, (int(corner1[0]), int(corner1[1])), (int(corner2[0]), int(corner2[1])), rgb_black, 2) 
                    #draw_half_circle_no_round(frame)
                    return corner1, corner2
                elif num_corner == 2:
                    # reset values
                    corner1 = corner2 = []
                    num_corner = 0
            elif len(approx) == 4 and color !='black':
                flag = 0
                n = approx.ravel()
                i = 0
                aux = 0
                vx_coord = []
                vy_coord = []
                for j in n :
                    if(i % 2 == 0):
                        x = n[i]
                        y = n[i + 1] 
                        # this verifies that every vertex is in the region of the viewport 
                        if (vpc.u_max > x > vpc.u_min) and (vpc.v_min > y > vpc.v_max):
                            flag = flag + 1  
                            vx_coord.append(x)
                            vy_coord.append(y)
                            # coordenadas de cada vertice
                            string = str(x) + " " + str(y) 
                            cv2.putText(frame, string, (x, y), 1, 0.5, rgb_black) 
                    i = i + 1
                if flag == 4:  
                    cv2.drawContours(frame, [approx], 0, (0), 2)

                    # computes the centroid   
                    cx, cy = centroid(count)
                    cv2.circle(frame,(int(cx),int(cy)),3,(rgb_white),-1)
                    # convert position (cx cy) and (vx, vy) to world coordinates        
                    cx2, cy2 = utils.vp2w(cx, cy, vpc) # manda centroide de objetos en pixeles
                    print("Posicion real: "+str(cy2)+" "+str(cx2)) # 8 y 9 s
                    # frame y count 
                    # Find the orientation of each shape
                    orientacion = getOrientation(count, frame)
                    print("Orientacion antes de pulsos: ")
                    print(orientacion)

                    #COMPROBAR QUE ME LLEGAN PARAMETROS DIFERENTES 
                    print("PARAMETROS")
                    difx = diferencial(cy2,centro[0])
                    dify = diferencial(cx2,centro[1])
                    print(color)
                    print(difx,dify)


                    if((difx>2 or difx<-1) and (dify>2 or dify<-2)): # si no es la posicion del ultimo jenga, ejecuta. 

                        # Calibracion del robot segun su posicion fisica. 
                        orientacion, aux = calibration(cx2,cy2,orientacion)
                
                        print("Orientacion modificada: "+str(orientacion))
                        # INGRESA FUNCION PARA TRANSFORMAR A PULSOS Y GUARDAR EN ARRAY 
                        #se invierte, para tener y como negativo y x como positivo 
                        pulsos,newQ5 = arm.solucion(cy2,cx2,aux,orientacion)
                        
                        print("llamado de pulsos: ")
                        print(pulsos,newQ5)
                        # INGRESA FUNCION DE C++ PARA ENVIAR EL ARRAY CON LOS PULSOS 
                        command_1 = 'gcc MaestroSerialExampleCWindows.c -o myprog'    
                        os.system(command_1)
                        command_2 = 'start myprog ' +str(pulsos[0])+' '+str(pulsos[1])+' '+str(pulsos[2])+' '+str(pulsos[3]) +' '+str(pulsos[4]) +' '+str(destino)+' '+str(newQ5)
                        os.system(command_2)

                    new_agent = utils.Agent(color) # guardo el color detectado en new_agent 
                        # 
                    new_agent.set_values(cy2, cx2, orientacion,aux) # x,y,orientacion 
                    #print(new_agent.cx)
                    time.sleep(10)
                    
                    # create agent in the world
                    global agent  
                    utils.agent[color] = new_agent 
                    min_prev = [] 
                    max_prev = [] 

                    return new_agent # retorna a managent
                else:
                    return False
                    
    return                 

def main():
    sg.theme('Black')
    # create the window and show it without the plot
    window = sg.Window('LUBOT', main_layout(), element_justification='c', location=(350, 100))
    #indicates which camera use
    cap = cv2.VideoCapture(0)
    recording = False
    app = App()
    app.mainloop()
    i = 0

    # Event loop that reads and displays frames 
    while True:
        event, _ = window.read(timeout=20) 
        
        # if event == 'Exit' or event == sg.WIN_CLOSED:
        #     if recording:
        #         cap.release()
        #     return
        if app.aux != 1 or app.aux==None or event == sg.WIN_CLOSED: # No presiono start  app.aux != 1 or app.aux==None or event == sg.WIN_CLOSED:
            if recording:
                cap.release()
                recording = False
            return 
        elif app.aux == 1: # Presiono start correctamente  app.aux == 1:
            recording = True
        
        # elif event == 'Start': 
        #     recording = True 
        if recording: 
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the camera autofocus off
            _, frame = cap.read() 
            # converting image obtained to hsv, if exists
            if frame is None:
                print('Something went wrong trying to connect to your camera. Please verify.')
                return
            else:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
            centro = [0,0]
            destino = 0
            region = pool.apply_async(generate_mask, (frame, hsv, 'black',centro,destino))
            region = region.get()  
            if region: 
                # print(region) 
                min_corner, max_corner = region # min corner tiene x.y minimo en pixeles, maxconer tiene x.y maximo en pixeles

                # define vpc values
                vpc.set_values(min_corner[0], min_corner[1], max_corner[0], max_corner[1]) 

                # convert limits coordinates to window (main layout)
                vpc_min  = utils.vp2w(min_corner[0], min_corner[1], vpc)  # guarda x,y real de la esquina inferior
                vpc_max  = utils.vp2w(max_corner[0], max_corner[1], vpc)  # guarda x,y real de la esquina superior

                if vpc_min and vpc_max:
                    cv2.putText(frame, (str(int(vpc_min[0]))+','+str(int(vpc_min[1]))), (int(vpc.u_min) - 10, int(vpc.v_min) + 15), 3, 0.5, rgb_black)
                    cv2.putText(frame, (str(int(vpc_max[0]))+','+str(int(vpc_max[1]))), (int(vpc.u_max) - 70, int(vpc.v_max) - 5), 3, 0.5, rgb_black)
                    x1 = 0
                    y1 = 10.5
                    x2, y2 = utils.w2vp(x1,y1, vpc)

                    #cv2.circle(frame,(int(centro[0]),int(centro[1])),5,(rgb_black),-1)

                    area_trabajo(frame ,min_corner ,max_corner, x2)
                    # 
                    # call to function to detect objects 
                    global cent
                    resultado,centro = manage_agent(frame, hsv,app.array,cent) 
                    cent = [centro[0],centro[1]]
                    #if(resultado == 0 and app.cantidad==i): break; # salir del ciclo while cuando ya haya llamado la misma cantidad
                    #else: i = i+1 
            
                    
                    
            #process image from camera
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()            
            window['image'].update(data=imgbytes)

        if cv2.waitKey(1) == ord('q'): # para cerrar la ventana y salir 
            break
                
if __name__=='__main__':
    t1 = threading.Thread(target=main)
    t1.start()
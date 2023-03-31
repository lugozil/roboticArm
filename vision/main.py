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
from tkinter import messagebox

pool = ThreadPool(processes=1)
# # viewport for camera
vpc = utils.ViewPort()
# rgb colors for opencv
rgb_black,rgb_white, cent, conteo= (0, 0, 0), (255, 255, 255), [0,0], 0

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
        self.logo_label = customtkinter.CTkLabel(self, text="Classification System",justify=customtkinter.CENTER ,font=customtkinter.CTkFont(size=25, weight="bold"))
        self.logo_label.place(x=70, y=20)

        self.label_1 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Enter number of items:",font=customtkinter.CTkFont(size=15))
        self.label_1.place(x=70, y=80)

        validate_entry = lambda text: text.isdecimal()
        self.entry_1 = customtkinter.CTkEntry(self, placeholder_text="Number of jengas",width=160,height=32,validate="key",validatecommand=(self.register(validate_entry), "%S"))
        self.entry_1.place(x=70, y=120)
        self.campo1 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="*",font=customtkinter.CTkFont(size=12))
        self.campo1.place(x=240, y= 125)

        self.label_2 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Activate the colors and indicate the destination:",font=customtkinter.CTkFont(size=15))
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

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text= "Confirm")
        self.checkbox_1.place(x=70, y=550)
        self.campo2 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="*",font=customtkinter.CTkFont(size=12))
        self.campo2.place(x=158, y= 550)

        self.button_1 = customtkinter.CTkButton(self, command=self.event_button_start, text="Start",font=customtkinter.CTkFont(size=15))
        self.button_1.place(x=130, y=600)

        self.button_help = customtkinter.CTkButton(self, command=self.event_button_help, text="Help",width=50,height=25,font=customtkinter.CTkFont(size=12))
        self.button_help.place(x=280, y=550)

        self.campo3 = customtkinter.CTkLabel(self, justify=customtkinter.CENTER,text="Required fields (*)",font=customtkinter.CTkFont(size=12))
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
        if(self.entry_1.get()!='' and self.checkbox_1.get()==1 and (self.switch_1.get()==1 or self.switch_2.get()==1 or self.switch_3.get()==1 or self.switch_4.get()==1 or self.switch_5.get()==1) and 
           (self.segmented_button_1.get()!='' or self.segmented_button_2.get()!='' or self.segmented_button_3.get()!='' or self.segmented_button_4.get()!='' or self.segmented_button_5.get()!='')):
            
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
    num+=1
    return num 

def diferencial(a,b):
    if(b==0):
        return 0 
    return ((b/a)*100)-100

def search(color,array2):
    lista = np.array(array2)
    posiciones = np.where(lista == color)
    posicion = int(posiciones[0])
    destino = array2[posicion][1] # me da el destino
    if(destino=='Left'): 
        destino = 1
    else:
        destino = 2

    return destino

def manage_agent(frame, hsv,array,centro):

    for color in utils.agent.keys(): # busca colores en los angentes
        for colores_activos in array: # 
            if color in colores_activos: # in colores_activos para buscar en toda la lista
                destino = search(color,array) 
                is_agent = generate_mask(frame, hsv, color,centro,destino) 
                if is_agent: 
                    centro = [is_agent.cx,is_agent.cy]

    return centro 

def pixelesextremos(corner1,corner2):
    aux1 = corner1[0]+corner1[1] 
    aux2 = corner2[0]+corner2[1]
    if(aux1>aux2):
        return corner2,corner1 
    else: 
        return corner1,corner2 

def radians2degrees(angle):
    return round((angle * 180 / math.pi), 2)

def calibration(cx2,cy2,orientacion):
    aux = auxorientacion = 0 
# MODIFICACIONES PARA AJUSTAR ORIENTACION Y PRECISION DEL ROBOT SEGUN UBICACION FISICA (CALIBRACION)4

# Right
    if(cx2 > 4.5 and orientacion<=90.00): 
        auxorientacion = orientacion
        orientacion +=98
        aux = 1
        print("BANDERA: 1")
        if(cx2<5): orientacion += 4
        if(cx2 > 2 and cy2>14 and auxorientacion > 25 and auxorientacion <70): orientacion +=4
        elif(cx2>12 and auxorientacion >0 and auxorientacion <25): orientacion -=6

    elif(cx2 > 4.5 and orientacion>90.00): # cx = cy pq esta invertido 
        auxorientacion = orientacion
        orientacion -=82 
        aux = 1
        print("BANDERA: 2")
        if(cx2>4.5 and cx2<6.5): aux = 5
        if(cx2 > 12 and orientacion > 0 and orientacion <25): orientacion -=15 
        elif(cx2>10 and orientacion >25 and orientacion <50):
            orientacion -=9
            if(cx2>14): orientacion -=14
        elif(cx2>2 and cx2<9 and orientacion >50 and orientacion <70): orientacion +=5
        elif(cx2>9 and orientacion >50 and orientacion <70): orientacion -=21
        elif(cx2>2 and cx2<10 and orientacion > 70 and orientacion < 100): orientacion +=2
        elif(cx2>10 and orientacion >70 and orientacion <100): orientacion -=13

# Left
    if(cx2 < -4.5 and orientacion>90.00):  
        orientacion +=4  # cx = cy pq esta invertido
        aux = 2
        print("BANDERA: 3")
        if(cx2>-6): orientacion -=19
        if(cx2 < -12.5 and orientacion >110.00 and orientacion < 160.00):
            orientacion +=12
            aux = 3
        elif(cx2 > -12.5 and orientacion >110.00 and orientacion < 165.00): orientacion -=7
        elif(cx2 < -12.5 and orientacion > 165 and orientacion < 180):
            orientacion +=12
            aux = 3
            if(orientacion > 180): orientacion = 9
            if(cy2 >14):orientacion -=7
        elif(cx2<-4 and cx2 > -7 and orientacion>110): orientacion -=28
            
    elif(cx2 < -4.5 and orientacion < 90.00): 
        print("BANDERA: 4")
        aux = 2
        orientacion -=4
        if(cx2 < -12.5 and orientacion >20.00 and orientacion < 70.00):
            orientacion +=12
            aux = 3
        elif(cx2< -12.5 and orientacion > 0 and orientacion < 20.00):
            orientacion +=12 
            aux = 3
        if(cy2 > 14 and cx2 > -12.5 and orientacion >0 and orientacion <20.00):
            orientacion -=5
            if(cx2>-6.5): ((orientacion -10)*-1) +95
 
# Center
    if(cx2>-4.5 and cx2<1 and orientacion >=90): 
        print("BANDERA: 5")
        auxorientacion = orientacion 
        orientacion -=28
        aux = 2
        if(auxorientacion>90 and auxorientacion<115): orientacion -=11
        if(cx2<1.5 and cx2>-1.5): 
            orientacion -=11
            aux = 4
        if(auxorientacion >=115 and auxorientacion <=160): orientacion -=7
        elif(auxorientacion >160 and auxorientacion <=180): orientacion -=4

    elif(cx2>-4.5 and cx2<1 and orientacion <90):
        print("BANDERA: 6")
        auxorientacion = orientacion
        orientacion -=37 
        aux = 2
        if(auxorientacion>=30 and auxorientacion<=70):
            orientacion = orientacion 
            print("C 0")
        elif(auxorientacion>0 and auxorientacion<30):
            orientacion -=36
            if(auxorientacion<15):
                orientacion = ((orientacion -10 ) *-1)+93 
                print("Bandera 3")

# clasificacion del medio cuando cx2 > 1 hasta cx2<3.5
    if(cx2>1 and cx2<4.5 and orientacion >=90): 
        print("BANDERA: 7")
        aux = 6
        auxorientacion = orientacion
        orientacion -=50         
        print("derecho 1")
    elif(cx2>1 and cx2<4.5 and auxorientacion>110 and auxorientacion<155): orientacion +=3
    elif(cx2>1 and cx2<4.5 and auxorientacion>=155 and orientacion <180): orientacion -=4

    elif(cx2>1 and cx2<4.5 and orientacion <90):
        print("BANDERA: 8")
        auxorientacion = orientacion
        orientacion -=51
        aux = 2 
        if(auxorientacion>25 and auxorientacion<70): orientacion -=21
        elif(auxorientacion>0 and auxorientacion<=25): orientacion = ((orientacion-10)*-1) +95

    print(orientacion)
    time.sleep(10)

    return orientacion,aux

def getOrientation(pts, img):

  # Construct a buffer used by the pca analysis
  sz = len(pts)
  data_pts = np.empty((sz, 2), dtype=np.float64)
  for i in range(data_pts.shape[0]):
    data_pts[i,0] = pts[i,0,0]
    data_pts[i,1] = pts[i,0,1]
 
  # Perform PCA analysis
  mean = np.empty((0))
  mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
  angle = math.atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
  orientacion = radians2degrees(angle)
  if orientacion < 0: 
    orientacion = orientacion + 180 

  return  orientacion

def draw_half_circle_no_round(image):
    height, width = image.shape[0:2]
    # Ellipse parameters
    radius, angle, startAngle, endAngle, thickness = 100, 0, 180, 360, -1
    center = (width / 2, height - 25)
    axes = (radius, radius)
    cv2.ellipse(image, center, axes, angle, startAngle, endAngle, rgb_black, thickness)

def area_trabajo(frame ,min_corner ,max_corner, x2):
    centro = [x2,min_corner[1]]
    medida = centro[0] - min_corner[0]
    axes = (int(medida),int(medida))
    angle, startAngle,endAngle =0,0,-180
    center=(int(centro[0]),int(centro[1]))

    cv2.ellipse(frame, center, axes, angle, startAngle, endAngle, rgb_black,2)
    orige = (int(min_corner[0]),int(min_corner[1]))
    fin = (int(max_corner[0]),int(min_corner[1]))
    cv2.line(frame,orige,fin,rgb_black,2)

def generate_mask(frame, hsv, color,centro,destino):
    mask = cv2.inRange(hsv, np.array(data.HSV_COLORS[color][0]), np.array(data.HSV_COLORS[color][1])) 
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #variables to define the rectangle of viewport
    num_corner,newQ5,out = 0, 0, 0
    corner1,corner2 = [],[] 
    global min_prev, max_prev 

    for count in contours:  
        # using functions to get the contour of shapes
        epsilon = 0.01 * cv2.arcLength(count, True)
        approx = cv2.approxPolyDP(count, epsilon, True)
        # get area to work with only visible objects solware y can cat 
        area = cv2.contourArea(count)
        if area > 150: 
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
                    corner1 = corner2 = []
                    num_corner = 0
            elif len(approx) == 4 and color !='black' and area>1000:
                flag = i = aux = 0
                n = approx.ravel()
                vx_coord =  vy_coord =[]

                for j in n :
                    if(i % 2 == 0):
                        x = n[i]
                        y = n[i + 1] 
                        # this verifies that every vertex is in the region of the viewport 
                        if (vpc.u_max > x > vpc.u_min) and (vpc.v_min > y > vpc.v_max):
                            flag+= 1  
                            vx_coord.append(x)
                            vy_coord.append(y)
                            # coordenadas de cada vertice
                            string = str(x) + " " + str(y) 
                            cv2.putText(frame, string, (x, y), 1, 0.5, rgb_black) 
                    i = i + 1
                if flag == 4:  
                    cv2.drawContours(frame, [approx], 0, (0), 2)
                    new_agent = utils.Agent(color) 
                    # computes the centroid   
                    cx, cy = centroid(count)
                    cv2.circle(frame,(int(cx),int(cy)),3,(rgb_white),-1)
                    # convert position (cx cy) and (vx, vy) to world coordinates        
                    cx2, cy2 = utils.vp2w(cx, cy, vpc) 
                    # Find the orientation of each shape
                    orientacion = getOrientation(count, frame)

                    #COMPROBAR QUE ME LLEGAN PARAMETROS DIFERENTES 
                    if(cy2>1 and cy2<-1):
                        difx = diferencial(cy2,centro[0])
                        dify = diferencial(cx2,centro[1])
                    else: 
                        difx = dify =3 
                    
                    if(cx2<4 and cx2>-4 and cy2<4): out = 1

                    if((difx>2 or difx<-1) and (dify>2 or dify<-2) and out!=1): # si no es la posicion del ultimo jenga, ejecuta. 
                        # Calibracion del robot segun su posicion fisica. 
                        orientacion, aux = calibration(cx2,cy2,orientacion)                
                        #se invierte, para tener y como negativo y x como positivo 
                        pulsos,newQ5 = arm.solucion(cy2,cx2,aux,orientacion)
                        if(newQ5!=0):
                            global conteo 
                            conteo = conteo+1
                            command_1 = 'gcc pololu.c -o myprog'    
                            os.system(command_1)
                            command_2 = 'start myprog ' +str(pulsos[0])+' '+str(pulsos[1])+' '+str(pulsos[2])+' '+str(pulsos[3]) +' '+str(pulsos[4]) +' '+str(destino)+' '+str(newQ5)
                            os.system(command_2)
                            time.sleep(9)
                            new_agent.set_values(cy2, cx2, orientacion,aux) 

                            global agent  
                            utils.agent[color] = new_agent 
                            min_prev = max_prev = []
                            return new_agent 
                        
                    new_agent.set_values(0,0,0,0)
                    return new_agent 
                else:
                    return False
                    
    return                 

def main():
    sg.theme('Black')
    window = sg.Window('LUBOT', main_layout(), element_justification='c', location=(350, 100))
    cap = cv2.VideoCapture(0)
    recording = False
    app = App()
    app.mainloop()
    i = 0

    # Event loop that reads and displays frames 
    while True:
        event, _ = window.read(timeout=20) 
        if app.aux != 1 or app.aux==None or event == sg.WIN_CLOSED: 
            if recording:
                cap.release()
                recording = False
            return 
        elif app.aux == 1: 
            recording = True

        if recording: 
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
            _, frame = cap.read() 

            if frame is None:
                print('Something went wrong trying to connect to your camera. Please verify.')
                return
            else:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
            centro, destino = [0,0], 0
            region = pool.apply_async(generate_mask, (frame, hsv, 'black',centro,destino))
            region = region.get()  
            if region: 
                min_corner, max_corner = region 
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
                    area_trabajo(frame ,min_corner ,max_corner, x2)
                    # call to function to detect objects 
                    global cent,conteo
                    centro = manage_agent(frame, hsv,app.array,cent) 
                    cent = [centro[0],centro[1]]
                    if(conteo==app.cantidad): #condition for exit
                        break
                              
            #process image from camera
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()            
            window['image'].update(data=imgbytes)

        if cv2.waitKey(1) == ord('q'): # close window and exit
            break
                
if __name__=='__main__':
    t1 = threading.Thread(target=main)
    t1.start()
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


pool = ThreadPool(processes=1)

# # viewport for camera
vpc = utils.ViewPort()

# rgb colors for opencv
rgb_black = (0, 0, 0)
rgb_white = (255, 255, 255)


def main_layout():
    # define the window layout
    layout = [[sg.Text('Virtual Environment', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 14'), 
               sg.Button('Exit', size=(10, 1),  font='Helvetica 14')]] 
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

def manage_agent(frame, hsv):
    for color in utils.agent.keys():   
        is_agent = generate_mask(frame, hsv, color) 

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

def generate_mask(frame, hsv, color):
    mask = cv2.inRange(hsv, np.array(data.HSV_COLORS[color][0]), np.array(data.HSV_COLORS[color][1])) # detecta el color que tiene
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
        # get area to work with only visible objects
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
                    #cv2.rectangle(frame, (int(corner1[0]), int(corner1[1])), (int(corner2[0]), int(corner2[1])), rgb_white, 2) 
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
                    orientacion = orientacion - 90 #si es negativo gira a la izq y si es positivo gira a la derecha
                    print("Orientacion: "+str(orientacion))

                    # INGRESA FUNCION PARA TRANSFORMAR A PULSOS Y GUARDAR EN ARRAY 
                    #se invierte, para tener y como negativo y x como positivo 
                    pulsos,newQ5 = arm.solucion(cy2,cx2,0,orientacion)
                    print(pulsos,newQ5)
                    # INGRESA FUNCION DE C++ PARA ENVIAR EL ARRAY CON LOS PULSOS 
                    # se envia c++(pulsos[0],pulsos[1],pulsos[2],pulsos[3],pulsos[4], destino, newQ5)
                    # pulsos = movimiento del robot 
                    # destino = izq o derecha 
                    # newQ5 = pulso que debe mover a5 para quedar perpendicular al eje piso. 
                    # time.sleep(20)






                    # display info on frame 
                    # info = str(cx2)+' | '+ str(cy2)
                    new_agent = utils.Agent(color)
                    # 
                    # new_agent.set_values(cx2, cy2, 0) # x,y,orientacion 
                    
                    # create agent in the world
                    global agent  
                    utils.agent[color] = new_agent 
                    min_prev = [] 
                    max_prev = [] 
                        
                    return new_agent
                else:
                    return False
                    
    return                 

def main():
    sg.theme('Black')
    # create the window and show it without the plot
    window = sg.Window('Virtual Environment', main_layout(), element_justification='c', location=(350, 100))
    #indicates which camera use
    cap = cv2.VideoCapture(0)
    recording = False
    # Event loop that reads and displays frames 
    while True:
        event, _ = window.read(timeout=20) 
        
        if event == 'Exit' or event == sg.WIN_CLOSED:
            if recording:
                cap.release()
            return
        
        elif event == 'Start': 
            recording = True 
        if recording: 
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the camera autofocus off
            _, frame = cap.read() 
            # converting image obtained to hsv, if exists
            if frame is None:
                print('Something went wrong trying to connect to your camera. Please verify.')
                return
            else:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
            region = pool.apply_async(generate_mask, (frame, hsv, 'black'))
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
                    manage_agent(frame, hsv)
            #process image from camera
            imgbytes = cv2.imencode('.png', frame)[1].tobytes() 
            window['image'].update(data=imgbytes)
                
if __name__=='__main__':
    t1 = threading.Thread(target=main)
    t1.start()
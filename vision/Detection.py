import cv2 
import numpy as np 
import imutils 
import time 

# colors 0,0,21,179,0,48
lower_yellow = np.array([25,70,120])
upper_yellow = np.array([30,255,255])

lower_green = np.array([55,111,0])
upper_green = np.array([82,255,255])

lower_red = np.array([0,50,120])
upper_red = np.array([10,255,255])

lower_blue = np.array([95,112,0])
upper_blue = np.array([119,255,255])

lower_black = np.array([0,0,21])
upper_black = np.array([179,255,87]) 

# viewport new values
NEW_MIN_X = 0
NEW_MIN_Y = -21
# real values in cm of projection
NEW_MAX_Y = 21
NEW_MAX_X = 21

#letra
font = cv2.FONT_HERSHEY_SIMPLEX

#Video
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480) 

#variables
amarillo = 0
list1 = []
i = 0
z = 2
contador = 0

# 0 a 480 / 640 a 0 

objeto = {
  "ID": 0,
  "COLOR": "",
  "CENTROIDE": [0,0],
  "ORIENTACION": 0,
}

def set_objeto(id,color,centroide,orientacion):
    objeto["ID"] = id 
    objeto["COLOR"] = color 
    objeto["CENTROIDE"] = centroide 
    objeto["ORIENTACION"] = orientacion

    return objeto 

def get_orientacion(array): 
    return 0

#busqueda de elemento en lista 
def search(lista,elemento): 
    for n in lista: 
      #  var = abs(n-elemento)
       # print("n-elemento: "+str(var))
        if abs(n-elemento)<=4: 
            return 0 
 
    return 1 


# funciones de colores, optimizar a una sola funcion donde se le pase la mascara y el color por parametros. 
def work_yellow(cnts1):
    global contador, amarillo, i 

    for c in cnts1: 
        area1 = cv2.contourArea(c)
        forma = "rectangle"
        if area1 > 1000: 
            peri = cv2.arcLength(c,True)
            obj = cv2.approxPolyDP(c,peri*0.02,True)
            if len(obj)==4:
                x,y,w,h = cv2.boundingRect(c)
                ratio = float(w)/h 
                if (ratio>=0.95 and ratio<=1.05): 
                    print("square")
                else:
                    cv2.drawContours(frame,[c],-1,(0,255,0),3) 
                    contador +=1
                                                       
                    M = cv2.moments(c)

                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    aux = cx+cy

                    array = [] 
                    array.append(cx)
                    array.append(cy)

                    cv2.circle(frame,(cx,cy),5,(255,255,255),-1)
                    cv2.putText(frame,"YELLOW", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(255,255,255),3)
                    i= i+1
                    
                    # llamado a funcion para obtener la orientacion
                   # orientacion = get_orientacion(array)

                    # llamado a funcion para llenar objeto  
                   # set_objeto(amarillo,'Y',array,orientacion) 
                   # print(objeto)
                   # time.sleep(20)

                    # llamado a funcion de C++ donde la paso objeto[cx,cy,z] donde x,y ya son coordenadas del mundo real
                    # set_servocomandos(xo,yo,zo,xd,yd,zd) o = origen, d= destino 


                    if (search(list1,aux)!=0):
                        amarillo+=1
                        list1.append(aux)
    #fin del ciclo 

    #cv2.putText(frame,f'Total: {contador}',(5,30),font,1,(255,0,255),2,cv2.LINE_AA)
    #print("Contenido final de lista con la suma de los centroides luego de terminar bucle for: "+str(list1))
    #print("Numero total de objetos amarillos: "+str(amarillo))
    #time.sleep(20)

def work_green(cnts2): 

    for c in cnts2: 
        area2 = cv2.contourArea(c)
        forma = "rectangle"
        if area2 > 1000: 

            peri = cv2.arcLength(c,True)
            obj = cv2.approxPolyDP(c,peri*0.02,True)
            if len(obj)==4:
                x,y,w,h = cv2.boundingRect(c)
                ratio = float(w)/h 
                if (ratio>=0.95 and ratio<=1.05): 
                    print("square")
                else:
                    cv2.drawContours(frame,[c],-1,(0,255,0),3)
                    M = cv2.moments(c)

                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    print("centroide objeto: ")
                    print(cx,cy)

                    cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                    cv2.putText(frame,"green and rect", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5,(255,255,255),3)

def work_red(cnts3): 
    for c in cnts3: 
        area3 = cv2.contourArea(c)
        forma = "rectangle"
        if area3 > 1000: 

            peri = cv2.arcLength(c,True)
            obj = cv2.approxPolyDP(c,peri*0.02,True)
            if len(obj)==4:
                x,y,w,h = cv2.boundingRect(c)
                ratio = float(w)/h 
                if (ratio>=0.95 and ratio<=1.05): 
                    print("square")
                else:
                    cv2.drawContours(frame,[c],-1,(0,255,0),3)
                    M = cv2.moments(c)

                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])

                    cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                    cv2.putText(frame,"red and rect", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5,(255,255,255),3)

def work_blue(cnts4): 

    for c in cnts4: 
        area4 = cv2.contourArea(c)
        forma = "rectangle"
        if area4 > 1000: 

            peri = cv2.arcLength(c,True)
            obj = cv2.approxPolyDP(c,peri*0.02,True)
            if len(obj)==4:
                x,y,w,h = cv2.boundingRect(c)
                ratio = float(w)/h 
                if (ratio>=0.95 and ratio<=1.05): 
                    print("square")
                else:
                    cv2.drawContours(frame,[c],-1,(0,255,0),3)
                    M = cv2.moments(c)

                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])

                    cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                    cv2.putText(frame,"Blue and rect", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5,(255,255,255),3)

def work_black(cnts5): 

    for c in cnts5: 
        area2 = cv2.contourArea(c)
        forma = "rectangle"
        if area2 > 50: 

            peri = cv2.arcLength(c,True)
            obj = cv2.approxPolyDP(c,peri*0.02,True)
            if len(obj)==4:
                x,y,w,h = cv2.boundingRect(c)
                ratio = float(w)/h 
                if (ratio>=0.95 and ratio<=1.05): 
                    print("square")
                else:
                    cv2.drawContours(frame,[c],-1,(0,255,0),3)
                    M = cv2.moments(c)

                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    print("centroide objeto: ")
                    print(cx,cy)

                    cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                    cv2.putText(frame,"black rect", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5,(255,255,255),3)


if __name__ == "__main__":
    while True: 
        _,frame = cap.read()
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        #filters 
        mask1 = cv2.inRange(hsv,lower_yellow,upper_yellow)
        mask2 = cv2.inRange(hsv,lower_green,upper_green)
        mask3 = cv2.inRange(hsv,lower_red,upper_red)
        mask4 = cv2.inRange(hsv,lower_blue,upper_blue)
        maskBlack = cv2.inRange(hsv,lower_black,upper_black)

        mask1 = cv2.GaussianBlur(mask1, (5,5), 0)
        mask2 = cv2.GaussianBlur(mask2, (5,5), 0)
        mask3 = cv2.GaussianBlur(mask3, (5,5), 0)
        mask4 = cv2.GaussianBlur(mask4, (5,5), 0)



        #contours 
        cnts1 = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = imutils.grab_contours(cnts1) 

        cnts2 = cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts2 = imutils.grab_contours(cnts2)

        cnts3 = cv2.findContours(mask3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts3 = imutils.grab_contours(cnts3)

        cnts4 = cv2.findContours(mask4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts4 = imutils.grab_contours(cnts4)

        cntsBlack = cv2.findContours(maskBlack,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cntsBlack = imutils.grab_contours(cntsBlack)

        #cv2.imshow("result",maskBlack)
        #imagen_reducida(cntsBlack)


        #llamado segun la funcionalidad del usuario 
        # 1. Clasificar solo un color 
        # 2. Clasificar todos los colores 
        # 3. Clasificar por orden de colores 

        work_yellow(cnts1)
        #work_green(cnts2)
        #work_red(cnts3)
        work_blue(cnts4)
        work_black(cntsBlack)

        # mostrar cuantos objetos se encontraron y cuantos de cada color. 
                    

        cv2.imshow("result",frame)
        k = cv2.waitKey(5)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
        






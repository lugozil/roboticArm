import cv2
import numpy as np
import tkinter as tk
# cambio en la rama test

# para comentar ctrl+k+c y descomentar ctrl+k+u
# Cargar el video
cap = cv2.VideoCapture(0)
hmin = 0 
smin = 0 
vmin = 0 
hmax = 179
smax = 255
vmax = 255

def nothing(x):
    pass

cv2.namedWindow('Imagen')
cv2.createTrackbar('Hue Min', 'Imagen',hmin,179,nothing)
cv2.createTrackbar('Hue Max', 'Imagen',hmax,179,nothing)
cv2.createTrackbar('Sat Min', 'Imagen', smin, 255,nothing)
cv2.createTrackbar('Sat Max', 'Imagen', smax, 255,nothing)
cv2.createTrackbar('Val Min', 'Imagen', vmin, 255,nothing)
cv2.createTrackbar('Val Max', 'Imagen', vmax, 255,nothing)

# Loop para procesar cada frame del video
while True:
    # Leer el frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convertir el frame a espacio de color HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hmin = cv2.getTrackbarPos('Hue Min','Imagen')
    hmax = cv2.getTrackbarPos('Hue Max','Imagen')
    smin = cv2.getTrackbarPos('Sat Min','Imagen')
    smax = cv2.getTrackbarPos('Sat Max','Imagen')
    vmin = cv2.getTrackbarPos('Val Min','Imagen')
    vmax = cv2.getTrackbarPos('Val Max','Imagen')


    lower1 = np.array([hmin, smin, vmin]) 
    upper1 = np.array([hmax, smax, vmax])
    
    lower_mask = cv2.inRange(hsv_frame, lower1, upper1)
    
    cv2.imshow('mask', lower_mask)
    #print(hmin,smin,vmin,hmax,smax,vmax)
    print(""+str(hmin)+", "+str(smin)+", "+str(vmin)+" | "+str(hmax)+", "+str(smax)+", "+str(vmax))

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()



# Probar un solo color en especifico. 
# while True:
#     # Leer el frame
#     ret, frame = cap.read() hhhy
#     if not ret:
#         break
    
#     # Convertir el frame a espacio de color HSV
#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     lower1 = np.array([20, 100, 100]) 
#     upper1 = np.array([30, 255, 255])

#     lower_mask = cv2.inRange(hsv_frame, lower1, upper1)
    
#     cv2.imshow('mask', lower_mask)
#     if cv2.waitKey(1) == ord('q'): gfrrth
#         break

# # Liberar la cámara y cerrar todas las ventanas
# cap.release()
# cv2.destroyAllWindows()
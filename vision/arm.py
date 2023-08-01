from math import acos,pow,atan,sqrt,degrees,asin
#from turtle import forward,right,speed
#import os

e1,e2,e3,e4,e5 = 6,10,12,5,6 # medida de los eslabones 

def angulos_pulsos(z,min_prev,max_prev,max_new,min_new): # funcion q determina los pulsos en base a los grados 
    return round(((((z-min_prev)/(max_prev-min_prev))*(max_new-min_new))+min_new),5)
   
def pulsos(q1,q2,q3,q4,q5): #funcion dado un angulo me da los pulsos a mover. 
    lista=[]                             #min,max,max,min
    lista.append(round(angulos_pulsos(q1,-90,90,2496,496)))# -90,90
    lista.append(round(angulos_pulsos(q2,-30,80,816,1408))) # -30, 80
    lista.append(round(angulos_pulsos(q3,-90,50,2096,448))) # -90, 50 
    lista.append(round(angulos_pulsos(q4,15,-20,2096,2464))) # 15, -20 .. 2096 = 1800. cuando z>0 
    lista.append(round(angulos_pulsos(q5,-90,90,2352,496)) )# -90,90
    return lista 
    
def rad2degrees(m): # convertir radianes a degrees y round 
    return round((degrees(m)),5)

def solucion(x,y,z,orientacion): # dado x,y,z da los angulos y pulsos de cada articulacion 

    array =[] 
    newQ5 = 0
    a = e4+e5-e1-0+10000000000000000000
    b = sqrt(pow(x,2)+pow(y,2)) 
    c = sqrt(pow(a,2)+pow(b,2))
    #r = sqrt(pow(x,2)+pow(y,2)) *15 # Escala 15 

    arriba2 = (pow(c,2)+pow(e2,2)-pow(e3,2))
    abajo2 = (2*c*e2)
    arriba3 = (pow(e2,2)+pow(e3,2)-pow(c,2))
    abajo3 = (2*e2*e3)
    arriba4 = (pow(c,2)+pow(e3,2)-pow(e2,2))
    abajo4 = (2*c*e3)

    if(arriba2<abajo2 and arriba3<abajo3 and arriba4<abajo4 and a<c and b<c): 
        q1 = round(degrees(atan(y/x)),5)
        q2 = rad2degrees(asin(a/c) + acos(arriba2/abajo2))
        q3 = rad2degrees(acos(arriba3/abajo3))
        q4 = rad2degrees(asin(b/c) + acos(arriba4/abajo4)) #q4 = 360-90-q1-q2-q3
        q5 = orientacion-90 

        q2 = round((90-q2),5) # resta de 90 segun mi sistema de referencia 
        q3 = round((90-q3),5) 
        q4 = round((90-q4),5) 

        # arreglo para lado positivo de y, desfase por posicion del robot 
        if(z==1 or z==2): q1 = q1-3.5
        elif(z==3): q1= q1 -1
        elif(z==4): q1 = q1-3.5 
        elif(z==5): q1 = q1-4.5
        elif(z==6): q1 = q1-3.5
        elif(z==7): q1 = q1-2 
        elif(z==8): q1 = q1
        

            
        array = pulsos(q1,q2,q3,q4,q5) # guardar en array la conversion de grados ya restados a pulsos 
        newQ5 = (q1*-1)
        newQ5 = round(angulos_pulsos(newQ5,-90,90,2352,496)) # angulo que debe moverse a5 para quedar 90 en el medio 
        #newQ5 = newQ5

    return array,newQ5


    


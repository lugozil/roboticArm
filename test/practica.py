import os 
import sys
sys.path.append("C:\\Users\\Lugozil\\Documents\GitHub\\roboticArm\\vision")
import arm 



x = 10.56
y = -6.82
z = 6 
aux = 20
orientacion = arm.solucion(x,y,z,aux)
print(orientacion)


import arm 
import os 
x = 10.56
y = -6.82
z = 2 
orientacion = 10 # 147.4 -3 8.63 -13.79

print(arm.solucion(x,y,z,orientacion))


# GUI 
command_1 = 'gcc MaestroSerialExampleCWindows.c -o myprog'    
os.system(command_1)
command_2 = 'start myprog '
result = os.system(command_2)

print("Resultado terminal: ")
print(result)


# constants
# colors in hsv dict for masks. the first value represents the lower limit and the second the lower
# Jenga hace referencia a los jengas marrones y Uno hace referencia a los jengas de Uno.( colores)
HSV_COLORS = {

    'black': [[0, 0, 21], [179,255,87]], # real

    # 'morado': [[0, 82, 141], [179, 255, 213]], # papel  alternativa: 95, 62, 139 | 179, 255, 255
    # 'morado': [[113, 29, 170], [175, 78, 243]], #cartulina morado claro

    # 'rosado': [[0, 80, 179], [179, 203, 255]], #papel 144, 80, 149 | 179, 203, 255

    'orange': [[0, 69, 127], [179, 255, 255]], #CARTULINA narnja
    #'orange': [[0, 69, 134], [179, 255, 255]], # naranja claro 
    
    #'brown': [[0, 68, 147], [55, 255, 235]], #alternativa 0, 75, 186 | 18, 144, 255
    'brown': [[4, 0, 85], [26, 156, 255]], # marron jenga

    #'red': [[0, 88, 116], [179, 255, 255]],
    'red': [[0, 78, 180], [46, 219, 255]], 

    'blue': [[0, 76, 189], [179, 255, 255]],
    'blue': [[90, 60, 0], [121, 255, 255]], # azul uno 

    'green': [[40, 69, 149], [179, 255, 229]],
    'green': [[0, 69, 141], [179, 255, 255]], #verde claro
    'green': [[46, 85, 63], [84, 255, 255]] # verde uno

}

#0,200,123,  179,255,176

# viewport new values
NEW_MIN_X = -21
NEW_MIN_Y = 0
# real values in cm of projection
NEW_MAX_Y = 21
NEW_MAX_X = 21

import data

# utils for classes and conversion functions  

# colors of agent triangles
agent = {'orange': None,
         'brown': None, 
         'red': None,
         'blue': None,
         'green': None
         }  

#classes definition
class ViewPort:
    def __init__(self):
        self.u_min = self.u_max = self.v_min = self.v_max = self.du = self.dv = None
    def set_values(self,  u_min, v_min, u_max, v_max):
        self.u_min = u_min
        self.u_max = u_max     
        self.v_min = v_min
        self.v_max = v_max
        self.du = u_max - u_min
        self.dv = v_min - v_max
    
class Agent:
    def __init__(self, color): 
        self.color = get_id(color)
        self.cx = self.cy = self.orientacion = self.line2 = self.line1 = self.limit = self.radius = self.info = self.aux =None 
    def set_values(self, cx, cy, orientacion,aux): 
        self.cx = cx
        self.cy = cy 
        #self.radius = r 
        #self.direction = direction
        self.orientacion = orientacion
        self.aux = aux

#utils functions
def get_id(color):
    agent_id = 0
    for col in agent.keys():
        agent_id = agent_id + 1 
        if col == color:  
            return agent_id    
        
# viewport to window function
def vp2w(x, y, VP):
    if VP.du > 0 and VP.dv > 0:
        value_x = round(((x - VP.u_min) * (data.NEW_MAX_X - data.NEW_MIN_X) / VP.du) + data.NEW_MIN_X, 2)
        diff_y = VP.v_min - y
        value_y = round((diff_y * (data.NEW_MAX_Y - data.NEW_MIN_Y) / VP.dv) + data.NEW_MIN_Y, 2)
        return value_x, value_y 
    else:
        return None

# window to viewport function
def w2vp(x, y, VP):
    div_x = data.NEW_MAX_X - data.NEW_MIN_X
    div_y = data.NEW_MAX_Y - data.NEW_MIN_Y
    if div_x > 0 and div_y > 0:
        value_x = round(((x - data.NEW_MIN_X) * VP.du / div_x) + VP.u_min, 2)  
        diff_y = data.NEW_MIN_Y - y
        value_y = round((diff_y * VP.dv / div_y) + VP.v_min, 2)
        return value_x, value_y     
    else:
        return None
    
def nuevomundo(x,y): 
    xreal =0 
    yreal =0
    return xreal,yreal 



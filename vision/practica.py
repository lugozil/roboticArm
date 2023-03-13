# import arm 

# x = 6.65
# y = 12.3
# z = 1 
# orientacion = 148.72 # 147.4 -3 

# print(arm.solucion(x,y,z,orientacion))


# GUI 
import tkinter as tk

class DragDropButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind('<Button-1>', self.on_button_press)
        self.bind('<B1-Motion>', self.on_button_motion)
        self.bind('<ButtonRelease-1>', self.on_button_release)
        self.dragging = False

    def on_button_press(self, event):
        self.dragging = True
        self.start_x = event.x_root
        self.start_y = event.y_root

    def on_button_motion(self, event):
        if self.dragging:
            x = self.winfo_x() + event.x_root - self.start_x
            y = self.winfo_y() + event.y_root - self.start_y
            self.place(x=x, y=y)

    def on_button_release(self, event):
        self.dragging = False

root = tk.Tk()

button1 = DragDropButton(root, text='Button 1')
button2 = DragDropButton(root, text='Button 2')
button3 = DragDropButton(root, text='Button 3')

button1.pack(side=tk.TOP, fill=tk.X)
button2.pack(side=tk.TOP, fill=tk.X)
button3.pack(side=tk.TOP, fill=tk.X)

root.mainloop()

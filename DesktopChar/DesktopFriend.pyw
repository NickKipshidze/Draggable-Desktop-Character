import tkinter, sys
from time import sleep
from os import path
from pyautogui import position
from random import randint

root = tkinter.Tk()
root.title("")
root.configure(background = "white")
root.attributes("-fullscreen", True)
root.attributes("-transparentcolor", "white")
root.wm_attributes("-topmost", 1)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)

class DragManager():
    global widget, offset, charDrag
    offset = -100
    
    def add_dragable(self, item, ofs):
        global widget, offset
        offset = ofs
        widget = item
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        global charDrag
        charDrag = True
        posX, posY = position()
        widget.place(x=posX+offset, y=posY+offset)

    def on_drag(self, event):
        posX, posY = position()
        widget.place(x=posX+offset, y=posY+offset)

    def on_drop(self, event):
        global charDrag
        charDrag = False
        posX, posY = position()
        widget.place(x=posX+offset, y=posY+offset)
        x,y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x,y)
        try:
            target.configure(image=event.widget.cget("image"))
        except:
            pass

class char():
    def physics():
        global charXFling, charX, scrX, scrY, charDrag
        
        if charXFling < -50: charXFling = -50
        if charXFling > 50: charXFling = 50
        
        if lbl_char.winfo_rooty() < scrY and charDrag == False:
            if charXFling > 0: charXFling -= 2
            if charXFling < 0: charXFling += 2
            if charXFling == 1: charXFling = 0
            charX = lbl_char.winfo_rootx()+charXFling
            if charX > scrX-200 or charX < 0: charX = lbl_char.winfo_rootx()
            lbl_char.place(x=charX, y=lbl_char.winfo_rooty()+20)
        elif charDrag == False:
            lbl_char.place(y=scrY)
            
    def chat():
        rng = randint(1, 1000)
        if rng == 1:
            print("hello")

img_char = tkinter.PhotoImage(file = resource_path("Duck.png"))
scrX, scrY = root.winfo_screenwidth(), root.winfo_screenheight()-200
charDrag, charXFling = False, 0

lbl_char = tkinter.Label(root, bg="white", image=img_char); lbl_char.place(x=100, y=scrY)

dnd = DragManager()
dnd.add_dragable(lbl_char, -100)

while True:
    posX = position()[0]
    sleep(0.00001)
    if charDrag == True: charXFling = position()[0]-posX
    
    try: root.update(); root.wm_attributes("-topmost", 1)
    except: break

    char.physics()
    char.chat()

root.mainloop()

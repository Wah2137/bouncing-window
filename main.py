
from tkinter import *

def start_drag(event):
    global Dragging, originx, originy
    Dragging = True
    originx = event.x
    originy = event.y

def stop_drag(event):
    global Dragging, yv, xv, pos_sample
    Dragging = False
    x_average = 0
    y_average = 0
    if len(pos_sample) == True:
        return 0
    for a in range(len(pos_sample) - 1):
        if x_average == 0:
            x_average = pos_sample[a][0] - pos_sample[a + 1][0]
        else:
            y_average = (y_average + pos_sample[a][0] - pos_sample[a + 1][0])/2
        if y_average == 0:
            y_average = pos_sample[a][1] - pos_sample[a + 1][1]
        else:
            y_average = (y_average + pos_sample[a][1] - pos_sample[a + 1][1])/2
    xv = -x_average
    yv = -y_average
    pos_sample = []


def on_drag(event):
    global Dragging, originx, originy,x , y, pos_sample
    if Dragging:
        x = window.winfo_x() - originx + event.x
        y = window.winfo_y() - originy + event.y
        if y < 0:
            y = 0
        window.geometry(f"+{x}+{y}")
    if len(pos_sample) >= 3:
        pos_sample.pop(0)
        pos_sample.append([x, y])
        return 0
    pos_sample.append([x, y])


def window_position():
    global w, h, x, y, ws, hs, yv, xv, resistance, bouncyness
    bwy = hs - h
    # y coords
    if bwy - y < 20 and -1 < yv < 1 or y > 700:
        yv = 0
        y = bwy
    #fall
    if y + yv< bwy:
        y += yv
        yv += 3
    #bounce
    elif yv != 0 and y != bwy and yv -1 != 0:
        yv = (-1*yv)/bouncyness + 12
        y += bwy - y + yv
    else:
        yv = 0
        y = bwy
    if y + yv < 0:
        yv = -1*yv
        y = yv - y
    #x position
    if xv < 1 and xv > -1:
        xv = 0
    if xv < 0:
        xv = xv/resistance + 0.5
    elif xv > 0:
        xv = xv/resistance - 0.5
    x += round(xv)
    #wall
    if x < 0:
        xv = -xv
    if x > ws:
        xv = -xv


def update():
    global w, h, x, y, ws, hs, Dragging
    if Dragging != True:
        window_position()
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.after(7, update)

def move_rectangle():
    global rectangle_xv, rectangle_yv, w,h
    canvas.move(rectangle, rectangle_xv, rectangle_yv)
    if canvas.coords(rectangle)[2] > w:
        rectangle_xv = -4
    if canvas.coords(rectangle)[0] < 0:
        rectangle_xv = 4
    if canvas.coords(rectangle)[3] > h:
        rectangle_yv = -4
    if canvas.coords(rectangle)[1] < 0:
        rectangle_yv = 4


def update_canvas():
    #update canvas
    move_rectangle()
    window.after(100, update_canvas)

number_clicks = 0
window = Tk()
window.resizable(False, False)
window.attributes('-topmost', True)

#window position variables
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight()
w = 200 # width for the Tk root
h = 200 # height for the Tk root
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
yv = 0
xv = 0
bouncyness = 1.01
resistance = 1.001

#drag variables
Dragging = False
originx = 0
originy = 0
pos_sample = []

#canvas drawing
canvas = Canvas(window, background = "blue")
rectangle = canvas.create_rectangle(10, 10, 20, 20, fill = "white")
rectangle_xv = 4
rectangle_yv = 3
canvas.pack()
update_canvas()


window.bind("<ButtonPress-1>", start_drag)
window.bind("<ButtonRelease-1>", stop_drag)
window.bind("<B1-Motion>", on_drag)

update()
window.mainloop()
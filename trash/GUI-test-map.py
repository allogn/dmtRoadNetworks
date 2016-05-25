from tkinter import *

canvas = Canvas(width=1330, height=700, bg='yellow')

# pack the canvas into a frame/form
canvas.pack(expand=YES, fill=BOTH)

map = PhotoImage(file='map.png')

# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(0, 0, image=map, anchor=NW)

# run it ...
mainloop()

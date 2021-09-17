import tkinter as tk
from tkinter import font

TEXT_OFFSET = 5
BLOCK_OFFSET = 2
BLOCK_HEIGHT = 50
BLOCK_WIDTH = 450
WIN_HEIGHT = 650
WIN_WIDTH = 500
INDENT_SIZE = 30

location = 0

win = tk.Tk()
win.title = "nsd"
canvas = tk.Canvas(height=WIN_HEIGHT,width=WIN_WIDTH, bg="white", bd=0)

canvas.pack()

def rect(width: int, pos: int, indent:int = 0):
    canvas.create_polygon(
        BLOCK_OFFSET+indent*INDENT_SIZE, pos*BLOCK_HEIGHT+BLOCK_OFFSET,
        width+BLOCK_OFFSET,pos*BLOCK_HEIGHT+BLOCK_OFFSET,
        width+BLOCK_OFFSET,pos*BLOCK_HEIGHT+BLOCK_HEIGHT+BLOCK_OFFSET,
        BLOCK_OFFSET+indent*INDENT_SIZE,pos*BLOCK_HEIGHT+BLOCK_HEIGHT+BLOCK_OFFSET,
        fill="white", outline="black"
    )

def draw(text: str, indent: int = 0):
    global location
    rect(BLOCK_WIDTH-indent*INDENT_SIZE,location)
    canvas.create_text(
        BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET,
        location * BLOCK_HEIGHT + BLOCK_OFFSET - TEXT_OFFSET,
        text=text, anchor=tk.NW, font = font.Font(size=BLOCK_HEIGHT - (TEXT_OFFSET*2))
    )
    location += 1

try:
    f = open("nsd.txt", "r")
except FileNotFoundError:
    print("nsd.txt does not exist")
    exit()

for i in f:
    match i.lower().strip().split():
        case ["set", var_name, "=", var_value]:
            print("set", var_name, var_value)
            draw("set {} = {}".format(var_name,var_value))
        case ["loop"]:
            pass
        case ["for"]:
            pass
        case ["end"]:
            pass
        case ["if"]:
            pass
        case ["else"]:
            pass
        case ["endif"]:
            pass
        case stuf:
            draw(stuf)
f.close()
win.mainloop()
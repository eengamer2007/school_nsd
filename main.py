# importing libs
import tkinter as tk
from tkinter import font
import nsd_parser

# imporant variables
TEXT_OFFSET = 5
BLOCK_OFFSET = 2
BLOCK_HEIGHT = 50
BLOCK_WIDTH = 690
WIN_WIDTH = 700
WIN_HEIGHT = 650
INDENT_SIZE = 30

location = 0

# init tkinter window
win = tk.Tk()
win.title = "nsd"
# make tkinter canvas and add to window
canvas = tk.Canvas(height=WIN_HEIGHT,width=WIN_WIDTH, bg="white", bd=0)
canvas.pack()

# draw rectangles
def rect(width: int, pos: int, indent):
    canvas.create_polygon(
        BLOCK_OFFSET + indent * INDENT_SIZE, pos * BLOCK_HEIGHT + BLOCK_OFFSET,
        width + BLOCK_OFFSET, pos * BLOCK_HEIGHT + BLOCK_OFFSET,
        width + BLOCK_OFFSET, pos * BLOCK_HEIGHT + BLOCK_HEIGHT + BLOCK_OFFSET,
        BLOCK_OFFSET + indent * INDENT_SIZE, pos * BLOCK_HEIGHT + BLOCK_HEIGHT + BLOCK_OFFSET,
        fill="white", outline="black"
    )

def get_array_len(array) -> int:
    array_len = 0
    for i in array:
        if isinstance(i, list):
            array_len += get_array_len(i)
        else:
            array_len += 1
    return array_len

def if_stuf(statment, if_arr, else_arr, indent):
    usewidth = (BLOCK_WIDTH - indent * INDENT_SIZE) / 2
    if_arr_len = get_array_len(if_arr)
    else_arr_len = get_array_len(else_arr)
    if if_arr_len >= else_arr_len:
        length = if_arr_len
    else:
        length = else_arr_len
    rect(BLOCK_WIDTH-indent*INDENT_SIZE, location, indent)
    


def stuf(array, indent):
    global location
    array_len = get_array_len(array)
    canvas.create_line(
        BLOCK_OFFSET + indent * INDENT_SIZE,
        BLOCK_OFFSET + location * BLOCK_HEIGHT,
        BLOCK_OFFSET + indent * INDENT_SIZE,
        BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location),
    )
    canvas.create_line(
        BLOCK_OFFSET + indent * INDENT_SIZE,
        BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location),
        BLOCK_OFFSET + (indent - 1) * INDENT_SIZE,
        BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location),
    )
    for i in array:
        if isinstance(i, list):
            match i[0]:
                case "loop": 
                    canvas.create_text(
                        BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET,
                        BLOCK_OFFSET + BLOCK_HEIGHT * location + TEXT_OFFSET,
                        text="loop", font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
                        anchor=tk.NW
                    )
                    canvas.create_line(
                        BLOCK_OFFSET + INDENT_SIZE * (indent + 1),
                        BLOCK_OFFSET + (location + 1) * BLOCK_HEIGHT,
                        BLOCK_OFFSET + BLOCK_WIDTH - (indent - 1) * INDENT_SIZE,
                        BLOCK_OFFSET + BLOCK_HEIGHT * (location + 1),
                    )
                    location += 1
                    stuf(i[1:], indent + 1)
                case "for": 
                    canvas.create_text(
                        BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET,
                        BLOCK_OFFSET + BLOCK_HEIGHT * location + TEXT_OFFSET,
                        text="for " + i[1], font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
                        anchor=tk.NW
                    )
                    canvas.create_line(
                        BLOCK_OFFSET + INDENT_SIZE * (indent + 1),
                        BLOCK_OFFSET + (location + 1) * BLOCK_HEIGHT,
                        BLOCK_OFFSET + BLOCK_WIDTH - (indent - 1) * INDENT_SIZE,
                        BLOCK_OFFSET + BLOCK_HEIGHT * (location + 1),
                    )
                    location += 1
                    stuf(i[2:], indent + 1)
                case "if":
                    if_stuf(i[1], i[2], i[3], indent)
                case _:
                    raise(KeyboardInterrupt)
        else:
            rect(BLOCK_WIDTH,location,indent)
            location += 1

def stuf_init(array):
    array_len = get_array_len(array)
    canvas.create_line(
        BLOCK_OFFSET + BLOCK_WIDTH,
        BLOCK_OFFSET + location * BLOCK_HEIGHT,
        BLOCK_OFFSET + BLOCK_WIDTH,
        BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location),
    )
    stuf(array, 0)

parsed = nsd_parser.nsd_parser_from_file("nsd.txt")
print(parsed)
stuf_init(parsed)

win.mainloop()
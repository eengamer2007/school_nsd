# importing libs
import tkinter as tk
from tkinter import font
import nsd_parser
import sys, os

#get input file name, handeling if file exist happens in nsd_parser.py
try:
    input_file = sys.argv[1]
    print("input file: " + input_file)
except IndexError:
    #default to nsd.txt if no file is given
    print("no input file given\nusing default: nsd.txt")
    input_file = "nsd.txt"

# global variables
TEXT_OFFSET = 5
BLOCK_OFFSET = 2
BLOCK_HEIGHT = 50
BLOCK_WIDTH = 690
WIN_WIDTH = 700
WIN_HEIGHT = 1000
INDENT_SIZE = 30

#make tkinter window, add canvas, make scroll bars
win=tk.Tk()
win.title = "nsd"
win.geometry("{}x{}".format(WIN_WIDTH + 20,650))
frame=tk.Frame(win, width=WIN_WIDTH, height=650)
frame.pack(expand=True, fill=tk.BOTH)
canvas=tk.Canvas(frame, bg='#FFFFFF',
    width=WIN_WIDTH, height=WIN_HEIGHT,
    scrollregion=(0, 0, WIN_WIDTH, WIN_HEIGHT))
hbar=tk.Scrollbar(frame, orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM, fill=tk.X)
hbar.config(command=canvas.xview)
vbar=tk.Scrollbar(frame, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
vbar.config(command=canvas.yview)
canvas.config(width=300, height=300)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

location = 0

# draw rectangles
def rect(width, pos, indent, indent_back = 0, indent_front = 0):
    canvas.create_polygon(
        BLOCK_OFFSET + indent * INDENT_SIZE + indent_front, pos * BLOCK_HEIGHT + BLOCK_OFFSET,
        width + BLOCK_OFFSET - indent_back, pos * BLOCK_HEIGHT + BLOCK_OFFSET,
        width + BLOCK_OFFSET - indent_back, pos * BLOCK_HEIGHT + BLOCK_HEIGHT + BLOCK_OFFSET,
        BLOCK_OFFSET + indent * INDENT_SIZE + indent_front, pos * BLOCK_HEIGHT + BLOCK_HEIGHT + BLOCK_OFFSET,
        fill="white", outline="black"
    )

#get the length of the array including sub arrays
def get_array_len(array) -> int:
    array_len = 0
    for i in array:
        if isinstance(i, list):
            if i[0] == "for":
                array_len += get_array_len(i[1:]) + 1
            elif i[0] == "if":
                array_len += 1
                array_len_1 = get_array_len(i[2])
                array_len_2 = get_array_len(i[3])
                if array_len_1 > array_len_2:
                    array_len += array_len_1
                else:
                    array_len += array_len_2
            else:
                array_len += get_array_len(i)
        else:
            array_len += 1
    return array_len

#drawing the block in an if statement
def if_pass(statment, if_arr, else_arr, indent, indent_back = 0):
    global location
    usewidth = (BLOCK_WIDTH - (indent) * INDENT_SIZE) / 2
    if_arr_len = get_array_len(if_arr)
    else_arr_len = get_array_len(else_arr)
    if if_arr_len >= else_arr_len:
        length = if_arr_len
    else:
        length = else_arr_len
    rect(BLOCK_WIDTH, location, indent, indent_back=indent_back)
    canvas.create_line(
        BLOCK_OFFSET + indent * INDENT_SIZE, location * BLOCK_HEIGHT + BLOCK_OFFSET,
        usewidth + BLOCK_OFFSET + indent * INDENT_SIZE,
        (location + 1) * BLOCK_HEIGHT + BLOCK_OFFSET
    )
    canvas.create_line(
        usewidth * 2 + BLOCK_OFFSET + indent * INDENT_SIZE,
        (location - 1) * BLOCK_HEIGHT + BLOCK_HEIGHT + BLOCK_OFFSET,
        usewidth + BLOCK_OFFSET + indent * INDENT_SIZE,
        (location + 1) * BLOCK_HEIGHT + BLOCK_OFFSET
    )
    canvas.create_text(
        usewidth + BLOCK_OFFSET + indent * INDENT_SIZE, (location) * BLOCK_HEIGHT + BLOCK_OFFSET,
        text = statment, font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
        anchor= tk.N
    )
    location += 1
    for i in range(length):
        rect(BLOCK_WIDTH, location, indent, indent_back=indent_back, indent_front=usewidth)
        rect(BLOCK_WIDTH, location, indent, indent_back=indent_back+usewidth)
        try:
            canvas.create_text(
                BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET,
                BLOCK_OFFSET + BLOCK_HEIGHT * location + TEXT_OFFSET,
                text= if_arr[i], font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
                anchor=tk.NW
            )
        except IndexError:
            pass
        try:
            canvas.create_text(
                BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET + usewidth,
                BLOCK_OFFSET + BLOCK_HEIGHT * location + TEXT_OFFSET,
                text= else_arr[i], font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
                anchor=tk.NW
            )
        except IndexError:
            pass
        location += 1
    
#drawing the blocks 
def standart_pass(array, indent, indent_back = 0, indent_front = 0, last = None):
    global location
    array_len = get_array_len(array)
    canvas.create_line(
        BLOCK_OFFSET + indent * INDENT_SIZE,
        BLOCK_OFFSET + location * BLOCK_HEIGHT,
        BLOCK_OFFSET + indent * INDENT_SIZE,
        BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location)
    )
    if last != "for":
        canvas.create_line(
            BLOCK_OFFSET + indent * INDENT_SIZE,
            BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location),
            BLOCK_OFFSET + (indent - 1) * INDENT_SIZE,
            BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location)
        )
    else_skip = 0
    for i in array:
        if isinstance(i, list):
            print(i)
            match i[0]:
                case "loop": 
                    canvas.create_text(
                        BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET,
                        BLOCK_OFFSET + BLOCK_HEIGHT * location + TEXT_OFFSET,
                        text="loop", font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
                        anchor=tk.NW
                    )
                    location += 1
                    standart_pass(i[1], indent + 1)
                case "while": 
                    canvas.create_text(
                        BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET,
                        BLOCK_OFFSET + BLOCK_HEIGHT * location + TEXT_OFFSET,
                        text="while "+i[1], font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
                        anchor=tk.NW
                    )
                    location += 1
                    standart_pass(i[2], indent + 1)
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
                        BLOCK_OFFSET + BLOCK_WIDTH - (indent) * INDENT_SIZE,
                        BLOCK_OFFSET + BLOCK_HEIGHT * (location + 1)
                    )
                    canvas.create_line(
                        BLOCK_OFFSET + INDENT_SIZE * (indent),
                        BLOCK_OFFSET + (location + get_array_len(i)) * BLOCK_HEIGHT,
                        BLOCK_OFFSET + BLOCK_WIDTH - (indent) * INDENT_SIZE,
                        BLOCK_OFFSET + BLOCK_HEIGHT * (location + get_array_len(i))
                    )
                    location += 1
                    standart_pass(i[2], indent + 1, last="for")
                    location += 1
                case "if":
                    if_pass(i[1], i[2], i[3], indent)
                    else_skip = 1
                case x:
                    print(x)
                    if not else_skip:
                        raise(KeyboardInterrupt)
        else:
            rect(BLOCK_WIDTH,location,indent, indent_back=indent_back)
            canvas.create_text(
                BLOCK_OFFSET + indent * INDENT_SIZE + TEXT_OFFSET,
                BLOCK_OFFSET + BLOCK_HEIGHT * location + TEXT_OFFSET,
                text= i, font = font.Font(size = -(BLOCK_HEIGHT - (TEXT_OFFSET * 2))),
                anchor=tk.NW
            )
            location += 1

#start the block drawing
def first_pass(array):
    array_len = get_array_len(array)
    canvas.create_line(
        BLOCK_OFFSET + BLOCK_WIDTH,
        BLOCK_OFFSET + location * BLOCK_HEIGHT,
        BLOCK_OFFSET + BLOCK_WIDTH,
        BLOCK_OFFSET + BLOCK_HEIGHT * (array_len + location),
    )
    standart_pass(array, 0)

parsed = nsd_parser.nsd_parser_from_file(input_file)
print(parsed)
first_pass(parsed)

#doesn't work
def to_png():
    print("made picture")
    canvas.postscript(file="nsd.gs")
    #why not work?: os.system("gswin32c -dNOPAUSE -sDEVICE=png16m -sOutputFile=nsd.png nsd.gs")
    #also not work
    #from PIL import Image
    #img = Image.open("nsd.gs")
    #img.save("nsd.png", "png")

win.after(1000, to_png)
win.mainloop()
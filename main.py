from graphics import *
import math

TEXT_OFFSET = 5
BLOCK_OFFSET = 2
BLOCK_HEIGHT = 50
BLOCK_WIDTH = 450
WIN_HEIGHT = 650
WIN_WIDTH = 500
INDENT_SIZE = 30

try:
    f = open("nsd.txt", "r")
except FileNotFoundError:
    print("nsd.txt does not exist")
    exit()

location = 0

win = GraphWin("nsd",WIN_WIDTH,WIN_HEIGHT)


def rect(width: int, pos: int, indent:int = 0):
    p = Rectangle(
        Point(BLOCK_OFFSET+indent*INDENT_SIZE,pos*BLOCK_HEIGHT+BLOCK_OFFSET),
        #Point(width+BLOCK_OFFSET,pos*BLOCK_HEIGHT+BLOCK_OFFSET),
        Point(width+BLOCK_OFFSET,pos*BLOCK_HEIGHT+BLOCK_HEIGHT+BLOCK_OFFSET),
        #Point(BLOCK_OFFSET+indent*INDENT_SIZE,pos*BLOCK_HEIGHT+BLOCK_HEIGHT+BLOCK_OFFSET)
    )
    p.draw(win)

def draw(text: str, indent: int = 0):
    global location
    rect(BLOCK_WIDTH-indent*INDENT_SIZE,location)
    t = Text(
        Point(BLOCK_OFFSET+indent*INDENT_SIZE+TEXT_OFFSET,location*BLOCK_HEIGHT+BLOCK_OFFSET+TEXT_OFFSET),
        text
    )
    size = BLOCK_HEIGHT-TEXT_OFFSET*2
    if size > 36:
        size = 36
    t.setSize(size)
    t.draw(win)
    location += 1


for i in f:
    match i.lower().strip().split():
        case ["set", var_name, "=", var_value]:
            print("set", var_name, var_value)
            draw("set")
        case _:
            print("unexpected command")
            exit()

win.getMouse()
win.close()
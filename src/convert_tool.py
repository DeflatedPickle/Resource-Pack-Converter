from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from main import main, conversion
import math
import sys

import os
print (os.getcwd())

global textures
textures = False

def center_window(win, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    win.geometry('%dx%d+%d+%d' % (width, height, x, y))
def selectRes():
    root.withdraw()

def convertionStart():
    res_win.withdraw()
    conversion(res_r.get())
    root.deiconify()
    center_window(root, 270, 120)
    messagebox.showinfo(title='success', message='Conversion is Done!')

def selectPack():
    global pack, textures
    pack = filedialog.askopenfilename(initialdir = "./",title = "Select Pack",filetypes = (("resource pack","*.zip"),("all files","*.*")))
    if(pack):
        root.withdraw()
        convert = main(pack[:-4], textures)
        if(convert == -1):
            print ("this pack is already compatible with 1.13")
            root.deiconify()
            center_window(root, 270, 120)
            messagebox.showwarning(title='warning', message="This pack is already compatible with 1.13, please select other!")
        elif(convert == 0):
            print ("please set it manually")
            res_win.deiconify()
            center_window(res_win, 270, 80)
            messagebox.showwarning(title='warning', message="Fail to detect the pack's resolution, please set it manually!")
        else:
            print ("next one?")
            root.deiconify()
            center_window(root, 270, 120)
            messagebox.showinfo(title='success', message='Conversion is Done!')
            return False

    else:
        print ('select pack to start conversion')

def fixtextures():
    global textures
    textures = not textures

def show_values(value=None):
    slider_label['text'] = 'resolution: '+ str(int(16 * math.pow(2, res_r.get()-1))) + 'X'
    #print (res_r.get())

root = tk.Tk()
root.title("Resource Pack Converter")
#root.geometry('500x300+500+200')
# root.resizable(width=False, height=False)
# center_window(root, 270, 120)
btn_select = tk.Button(
    root,
    text='Select Pack',
    width=50,
    height=10,
    command=selectPack
    )
btn_setNatural = tk.Checkbutton (
    root,
    text="Fix Boxcraft Textures",
    height=5,
    width=50,
    command=fixtextures
)
btn_select.pack()
btn_setNatural.pack()

res_win = tk.Toplevel(root)
res_win.title("Set Resolution")
res_win.resizable(width=False, height=False)
center_window(res_win, 270, 80)

''' resolution ratio set'''
res_r = tk.IntVar()
res_r.set(1)
slider_res = tk.PanedWindow(res_win)
slider_res.pack(fill = tk.BOTH, expand = 1)
slider_label = tk.Label(res_win, text='resolution: 16X')
slider_scale = tk.Scale(
    res_win,
    from_=0,
    to=6,
    orient=tk.HORIZONTAL,
    variable = res_r,
    command=show_values
    )

slider_res.add(slider_label)
slider_res.add(slider_scale)

btn_start = tk.Button(
    res_win,
    text='Confirm',
    width=60,
    command=fixtextures
    )
btn_start.pack()
res_win.withdraw()



root.mainloop()

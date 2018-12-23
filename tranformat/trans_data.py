#!coding:utf-8

from README import readme
from merge_csv import *
import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename

window = tk.Tk()
window.title('TRANS')
window.geometry('450x200')

# welcome image
#canvas = tk.Canvas(window, height=200, width=460)
#image_file = tk.PhotoImage(file=r'H:\tranformat\welcome.gif')
#image = canvas.create_image(0,0, anchor='nw', image=image_file)
#canvas.pack(side='top')

#select Input path 
def selectPath():
    path_ = askdirectory()
    var_input_dir.set(path_)
	
#sane file 
def savePath():
	_path = asksaveasfilename()
	var_out_name.set(_path)

# user information
tk.Label(window, text='INPUT PATH:').place(x=63, y= 50)
tk.Label(window, text='OUTPUT PATH:').place(x=50, y= 90)

var_input_dir = tk.StringVar()
#var_input_dir.set('Your data folder name!')
entry_input = tk.Entry(window, textvariable=var_input_dir)
entry_input.place(x=160, y=50)
btn_browse = tk.Button(window, text="BROWSE", width=10, command=selectPath)
btn_browse.place(x=310, y=45)
var_out_name = tk.StringVar()
#var_out_name.set('Your outfile name!')
entry_out = tk.Entry(window, textvariable=var_out_name)
entry_out.place(x=160, y=90)
btn_browse = tk.Button(window, text="SAVE", width=10, command=savePath)
btn_browse.place(x=310, y=85)

def show_readme():
    tk.messagebox.showinfo(title='README', message=readme)

def run_job():
    input_dir = var_input_dir.get()
    outfile = var_out_name.get()
    try:
        transformat(input_dir, outfile)
        tk.messagebox.showinfo(title='SUCCEED', message="JOB IS SUCCEED!")
    except FileNotFoundError as e:
        tk.messagebox.showerror(title="PATH ERROR", 
			message="Try Again\nNot Found Your Input PATH!")
    except:
        tk.messagebox.showerror(title="ERROR", 
			message='Somthing Error!\nyou can ask for: hanwei@shanghaitech.edu.cn')

# login and sign up button
btn_readme = tk.Button(window, text='README', width=10, command=show_readme)
btn_readme.place(x=55, y=150)
btn_submit = tk.Button(window, text='SUBMIT', width=10, command=run_job)
btn_submit.place(x=185, y=150)
btn_quit = tk.Button(window, text="QUIT", width=10, command=window.destroy)
btn_quit.place(x=310, y=150)

window.mainloop()


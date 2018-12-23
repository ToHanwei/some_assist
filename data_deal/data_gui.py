#!coding:utf-8

from README import readme
from INTER import inter_info
from data_calculation import *
import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename

window = tk.Tk()
window.title('SHUDATA')
window.geometry('450x300')

#select Input path 
def selectPath():
    path_ = askopenfilename()
    var_input_dir.set(path_)
	
#sane file 
def savePath():
	_path = asksaveasfilename()
	var_out_name.set(_path)

def Inter_info():
    tk.messagebox.showinfo(title="Internal Reference", message=inter_info)

def show_readme():
    tk.messagebox.showinfo(title='README', message=readme)

def run_job():
    inter = var_inter.get()
    inputfile = var_input_dir.get()
    outfile = var_out_name.get()
    try:
        data_conduct(inputfile, outfile, inter)
        tk.messagebox.showinfo(title='SUCCEED', message="JOB IS SUCCEED!")
    except FileNotFoundError as e:
        tk.messagebox.showerror(title="PATH ERROR", 
			message="Try Again\nNot Found Your Input PATH!")
    except KeyError as k:
        tk.messagebox.showerror(title="Key Rrror", 
			message="Maybe your columns name is Error! check:\ncontain name \"Sample Name, Target Name, CT\"")
    except:
        tk.messagebox.showerror(title="ERROR", 
			message='Somthing Error!\nyou can ask for: hanwei@shanghaitech.edu.cn')


# user information
tk.Label(window, text='INTERNAL:').place(x=86, y= 50)
tk.Label(window, text='INPUT:').place(x=109, y= 100)
tk.Label(window, text='OUTPUT:').place(x=98, y= 150)

var_inter = tk.StringVar()
var_inter.set('hprt')
entry_inter = tk.Entry(window, textvariable=var_inter)
entry_inter.place(x=160, y=50)
btn_browse = tk.Button(window, text="EXPLAIN", width=10, command=Inter_info)
btn_browse.place(x=310, y=45)

var_input_dir = tk.StringVar()
entry_input = tk.Entry(window, textvariable=var_input_dir)
entry_input.place(x=160, y=100)
btn_browse = tk.Button(window, text="BROWSE", width=10, command=selectPath)
btn_browse.place(x=310, y=95)

var_out_name = tk.StringVar()
entry_out = tk.Entry(window, textvariable=var_out_name)
entry_out.place(x=160, y=150)
btn_browse = tk.Button(window, text="SAVE", width=10, command=savePath)
btn_browse.place(x=310, y=145)


# login and sign up button
btn_readme = tk.Button(window, text='README', width=10, command=show_readme)
btn_readme.place(x=55, y=220)
btn_submit = tk.Button(window, text='SUBMIT', width=10, command=run_job)
btn_submit.place(x=185, y=220)
btn_quit = tk.Button(window, text="QUIT", width=10, command=window.destroy)
btn_quit.place(x=310, y=220)

window.mainloop()


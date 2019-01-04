#!coding:utf-8

from README import readme
from INTER import *
from data_calculation import *
import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename

window = tk.Tk()
window.title('SHUDATA')
window.geometry('450x360')

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
	
def Expr_info():
    tk.messagebox.showinfo(title="Experiment Reference", message=expr_info)

def show_readme():
    tk.messagebox.showinfo(title='README', message=readme)

def run_job():
    inter = var_inter.get()
    expr = var_expr.get()
    inputfile = var_input_dir.get()
    outfile = var_out_name.get()
    try:
        transDf(inputfile, outfile, inter, expr)
        tk.messagebox.showinfo(title='SUCCEED', message="JOB IS SUCCEED!")
    except FileNotFoundError as e:
        tk.messagebox.showerror(title="PATH ERROR", message=no_file)
    except KeyError as k:
        tk.messagebox.showerror(title="Key Rrror", message=key_error)
    except ValueError as z:
        tk.messagebox.showerror(title="Value Error", message=value_error)
    except:
        tk.messagebox.showerror(title="ERROR", message=some_other)


# user information
tk.Label(window, text='EXPER:').place(x=109, y=50)
tk.Label(window, text='INTERNAL:').place(x=86, y = 100)
tk.Label(window, text='INPUT:').place(x=109, y = 150)
tk.Label(window, text='OUTPUT:').place(x=98, y = 200)

var_expr = tk.StringVar()
var_expr.set("Gapdh-siRNA")
entry_input = tk.Entry(window, textvariable=var_expr)
entry_input.place(x=160, y = 50)
btn_browse = tk.Button(window, text="EXNAME", width=10, command=Expr_info)
btn_browse.place(x=310, y=45)

var_inter = tk.StringVar()
var_inter.set('hprt')
entry_inter = tk.Entry(window, textvariable=var_inter)
entry_inter.place(x=160, y = 100)
btn_browse = tk.Button(window, text="EXPLAIN", width=10, command=Inter_info)
btn_browse.place(x=310, y=95)

var_input_dir = tk.StringVar()
entry_input = tk.Entry(window, textvariable=var_input_dir)
entry_input.place(x=160, y = 150)
btn_browse = tk.Button(window, text="BROWSE", width=10, command=selectPath)
btn_browse.place(x=310, y=145)

var_out_name = tk.StringVar()
entry_out = tk.Entry(window, textvariable=var_out_name)
entry_out.place(x=160, y = 200)
btn_browse = tk.Button(window, text="SAVE", width=10, command=savePath)
btn_browse.place(x=310, y = 195)


# login and sign up button
btn_readme = tk.Button(window, text='README', width=10, command=show_readme)
btn_readme.place(x=55, y = 270)
btn_submit = tk.Button(window, text='SUBMIT', width=10, command=run_job)
btn_submit.place(x=185, y = 270)
btn_quit = tk.Button(window, text="QUIT", width=10, command=window.destroy)
btn_quit.place(x=310, y = 270)

window.mainloop()


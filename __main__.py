import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("tkagg")
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
import math
from tkinter import messagebox as tkMessageBox

MIN_STEPS = 100
MAX_STEPS = 10000
UPPER_BOUND = 9
X0_POSITION_X = 100
X0_POSITION_Y = 100
Y0_POSITION_X = 100
Y0_POSITION_Y = 125


class DrawOpt:
    def __init__(self):
        self.option = ""
        self.num_seg = 10
        self.INITIAL_X = 0
        self.INITIAL_Y = 1

    def update_option(self, event):
        l = event.widget
        sel = l.curselection()
        self.option = l.get(sel[0])

    def update_num_seg(self, event):
        self.num_seg = int(event)

def getD(opt):
    rt = math.sqrt(opt.INITIAL_Y)
    d = (- rt + 1)/math.exp(opt.INITIAL_X)
    d2 = (rt + 1)/math.exp(opt.INITIAL_X)
    if d>0 and  d2 > 0:
        assert(0)
    else:
        return max(d,d2)

def exact_sol(X, opt):
    D = getD(opt)
    return np.square(1-D*np.exp(X))


def fx(x,opt):
    D = getD(opt)

    return (1-D*math.exp(x))*(1-D*math.exp(x))


def f(x, y):
    return 2 * math.sqrt(y) + 2 * y


def approx_method(opt):  # returns two parameters:
    # one is pairs (X,Y) to plot,
    # second is the name of the method chosen.
    if (len(opt.option) == 0):  # default method
        return Eulers(opt)
    if (opt.option[0] == 'E'):
        return Eulers(opt)
    elif (opt.option[0] == 'I'):
        return ImprovedEulers(opt)
    else:
        return RungeKutta(opt)


def get_name_of_method(opt):
    if (len(opt.option) == 0):
        return "Euler's method:"
    if (opt.option[0] == 'E'):
        return "Euler's method:"
    elif (opt.option[0] == 'I'):
        return "Improved Euler's method:"
    else:
        return "Runge-Kutta method:"


def Eulers(opt):
    X = np.linspace(opt.INITIAL_X, UPPER_BOUND, opt.num_seg + 1)
    Y = []
    x_cur = opt.INITIAL_X
    y_cur = opt.INITIAL_Y

    Y.append(y_cur)
    h = (UPPER_BOUND - opt.INITIAL_X) / (opt.num_seg)
    for i in range(opt.num_seg):
        y_cur = y_cur + h * f(x_cur, y_cur)
        #g = f(x_cur, y_cur)
        Y.append(y_cur)
        x_cur += h

    Y = np.array(Y)
    #plt.plot(X, Y)
    return X, Y


def ImprovedEulers(opt):
    X = np.linspace(opt.INITIAL_X, UPPER_BOUND, opt.num_seg + 1)
    Y = []
    x_cur = opt.INITIAL_X
    y_cur = opt.INITIAL_Y
    Y.append(y_cur)
    h = (UPPER_BOUND - opt.INITIAL_X) / (opt.num_seg)
    for i in range(opt.num_seg):
        k1 = f(x_cur, y_cur)
        k2 = f(x_cur + h, y_cur + h * k1)
        y_cur = y_cur + h / 2 * (k1 + k2)
        Y.append(y_cur)
        x_cur += h
    Y = np.array(Y)
    return X, Y


def RungeKutta(opt):
    X = np.linspace(opt.INITIAL_X, UPPER_BOUND, opt.num_seg + 1)
    Y = []
    x_cur = opt.INITIAL_X
    y_cur = opt.INITIAL_Y
    Y.append(y_cur)
    h = (UPPER_BOUND - opt.INITIAL_X) / (opt.num_seg)
    for i in range(opt.num_seg):
        k1 = f(x_cur, y_cur)
        k2 = f(x_cur + h / 2, y_cur + h / 2 * k1)
        k3 = f(x_cur + h / 2, y_cur + h / 2 * k2)
        k4 = f(x_cur + h, y_cur + h * k3)
        y_cur = y_cur + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        Y.append(y_cur)
        x_cur += h
    Y = np.array(Y)
    return X, Y


def draw_graph(opt):
    try:
        opt.INITIAL_X = float(box_x.get())
        opt.INITIAL_Y = float(box_y.get())
    except:
        opt.INITIAL_X = 1
        opt.INITIAL_Y = 4
        box_x.insert(END, '1')
        box_y.insert(END, '4')
    opt.INITIAL_X = min(opt.INITIAL_X, UPPER_BOUND)
    draw_window = Tk()
    f = Figure()
    ax = f.add_subplot(111)

    # exact solution
    X = np.linspace(opt.INITIAL_X, UPPER_BOUND, MAX_STEPS)
    Y = exact_sol(X, opt)
    ax.plot(X, Y)

    # approx solution
    X1, Y1 = approx_method(opt)
    name_of_method = get_name_of_method(opt)
    draw_window.title(name_of_method + "two graphs")

    ax.plot(X1, Y1)
    canvas = FigureCanvasTkAgg(f, draw_window)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    draw_window.mainloop()


def draw_error_graph(opt):
    try:
        opt.INITIAL_X = float(box_x.get())
        opt.INITIAL_Y = float(box_y.get())
    except:
        opt.INITIAL_X = 1
        opt.INITIAL_Y = 3
    opt.INITIAL_X = min(opt.INITIAL_X, UPPER_BOUND)
    draw_window = Tk()
    f = Figure()
    ax = f.add_subplot(111)

    # approx solution
    X1, Y1 = approx_method(opt)
    name_of_method = get_name_of_method(opt)
    draw_window.title(name_of_method + "error graph")

    Y = exact_sol(X1, opt)

    # calculate error
    E = np.abs(Y1 - Y)
    ax.plot(X1, E)
    canvas = FigureCanvasTkAgg(f, draw_window)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    draw_window.mainloop()

def getMax(XX,YY,opt):
    ans = 0
    for i in range(0,len(XX)):
        ans = max(ans, abs(YY[i] - fx(XX[i],opt)))
    return ans

def getMaxErr(opt):
    YY = []
    XX = []
    for i in range(10, 1000, 10):
        opt.num_seg = i
        X1, Y1 = approx_method(opt)
        n = len(Y1)
        for j in range(0, n):
            Y1[j] = abs(Y1[j] - (1 - getD(opt) * math.exp(X1[j])) * (1 - getD(opt) * math.exp(X1[j])))
        YY.append(max(Y1))
        XX.append(i)
    return XX, YY


def draw_max_error_graph(opt):
    draw_window = Tk()
    name_of_method = get_name_of_method(opt)
    draw_window.title(name_of_method + "max error graph")
    f = Figure()
    previous_value = opt.num_seg
    ax = f.add_subplot(111)
    Mx_errors = []
    XX, YY = getMaxErr(opt)
    ax.plot(XX, YY)
   # plt.plot(X, Mx_errors)
    opt.num_seg = previous_value
    canvas = FigureCanvasTkAgg(f, draw_window)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    draw_window.mainloop()


def draw_all_error_graph(opt):
    draw_window = Tk()
    draw_window.title("all  error graph, Euler blue, Improved Euler Orange, RungeKutta green")
    f = Figure()
    opt.option = "Euler";
    ax = f.add_subplot(111)
    X1, Y1 = getMaxErr(opt)
    ax.plot(X1,Y1)
    opt.option = "Improved Euler"
    X1, Y1 = getMaxErr(opt)
    ax.plot(X1,Y1)
    opt.option = "RungeKutta"
    X1, Y1 = getMaxErr(opt)
    ax.plot(X1,Y1)
    canvas = FigureCanvasTkAgg(f, draw_window)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    draw_window.mainloop()



root = Tk()
root.minsize(600, 600)
root.maxsize(1200, 1200)
options = DrawOpt()

button = Button(root, text="draw graphs", command=lambda: draw_graph(options))
button.place(anchor="center", x=300, y=250)


button_error = Button(root,text="draw error graph", command=lambda:draw_error_graph(options))
button_error.place(anchor="center",x=300,y=275)

button_mx_error = Button(root,text="draw max error",command=lambda:draw_max_error_graph(options))
button_mx_error.place(anchor="center",x=300,y=300)


button_mx_error = Button(root,text="draw all errors",command=lambda:draw_all_error_graph(options))
button_mx_error.place(anchor="center",x=300,y=350)


method_list_box = Listbox(root, height=5, width=15, selectmode=SINGLE)
methods = ["Euler's method", "Improved Euler's method", "Runge-Kutta method"]
for i in methods:
    method_list_box.insert(END, i)
method_list_box.place(x=100, y=150)
method_list_box.bind("<<ListboxSelect>>", options.update_option)

step_scale = Scale(root, orient=HORIZONTAL, length=300, from_=10, to=1000, resolution=1, command=options.update_num_seg)
step_scale.place(x=100, y=50)

box_x = Entry(root, width=10)
box_x.place(x=X0_POSITION_X, y=X0_POSITION_Y)
box_x.insert(END, '0')

box_y = Entry(root, width=10)
box_y.place(x=Y0_POSITION_X, y=Y0_POSITION_Y)
box_y.insert(END, '1')

label_x = Label(root, text="x0:")
label_x.place(x=X0_POSITION_X - 70, y=X0_POSITION_Y)

label_y = Label(root, text="y0:")
label_y.place(x=Y0_POSITION_X - 70, y=Y0_POSITION_Y)

label_num = Label(root, text="number of steps:")
label_num.place(x=X0_POSITION_X - 100, y=X0_POSITION_Y - 30)

label_title = Label(root, text="y' = 2y^(1/2) + 2y")
label_title.place(x=300, y=10, anchor="center")
root.mainloop()

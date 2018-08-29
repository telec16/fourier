from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

import numpy as np

import tkinter as tk
LARGE_FONT= ("Verdana", 12)


class GraphPage:

	def __init__(self, master, type):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.type = type
		
		#self.master.overrideredirect(True)
		self.master.protocol("WM_DELETE_WINDOW", lambda: None)
		
		lblTitle = tk.Label(self.frame, text=type, font=LARGE_FONT)
		lblTitle.pack(pady=10,padx=10)
		
		plt.xkcd()
		fig = plt.figure()
		plt.ion()
		self.ax = fig.add_subplot(1,1,1)
		
		canvas = FigureCanvasTkAgg(fig, master=self.master)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		toolbar = NavigationToolbar2Tk(canvas, self.master)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		
	def update(self, o, v):
		t = np.linspace(0, 5*2*np.pi, 400)
		
		x = self.get_cos_sin_sum(t, v[0], v[1], o[0])
		y = self.get_cos_sin_sum(t, v[2], v[3], o[1])
		
		if self.type=="XY graph":
			self.update_XY_plot(t, x, y)
		else:
			self.update_T_plot(t, x, y)
		
	def update_XY_plot(self, t, x, y):
		self.ax.clear()
		
		self.ax.plot(x, y)

		plt.xlabel('X')
		plt.ylabel('Y')
		
	def update_T_plot(self, t, x, y):
		self.ax.clear()
		
		self.ax.plot(t, x, 'b')
		self.ax.plot(t, y, 'r')
		
		plt.xlabel('time')
		plt.ylabel('X:b; Y:r')
	
	def get_cos_sin_sum(self, timebase, coefs_c, coefs_s, offset):
		coss = [np.cos((i+1) * timebase) * c for i,c in enumerate(coefs_c)]
		sins = [np.sin((i+1) * timebase) * c for i,c in enumerate(coefs_s)]
		
		sum  = [np.sum(r[c] for r in sins) + np.sum(r[c] for r in coss) + offset for c in range(len(timebase))]
		
		return sum
		
		
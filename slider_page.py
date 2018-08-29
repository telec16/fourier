from graph_page import GraphPage

import tkinter as tk
from tkinter import ttk
LARGE_FONT= ("Verdana", 12)


class SliderPage:
	
	def __init__(self, master, slider_nb):
		self.pages = {}
		self.sliders_offset = [None for x in range(2)] 
		self.sliders = [[None for x in range(slider_nb)] for y in range(4)] 
		self.master = master
		self.extremum = 100
		
		header_frame = tk.Frame(self.master, pady=3)
		control_frame = tk.Frame(self.master, pady=3)
		preset_frame = tk.Frame(self.master, pady=3)
		slider_frame = tk.Frame(self.master, pady=3)
		
		header_frame.grid(row=0)
		control_frame.grid(row=1)
		preset_frame.grid(row=2)
		slider_frame.grid(row=3)
		
		#Header
		lblTitle = tk.Label(header_frame, text="Sliders", font=LARGE_FONT)
		lblTitle.grid(row=0, column=0, pady=10,padx=10)

		#Controls
		self.btnXY = tk.Button(control_frame, text="Open XY graph", command = lambda: self.new_graph_page("XY graph", self.btnXY))
		self.btnT = tk.Button(control_frame, text="Open time graph", command = lambda: self.new_graph_page("time graph", self.btnT))
		
		self.btnXY.grid(row=0, column=0)
		self.btnT.grid(row=0, column=1)
		
		#Preset
		btnClr = tk.Button(preset_frame, text="Clear", command = lambda: self.preset("clear"))
		btnSquare = tk.Button(preset_frame, text="Square", command = lambda: self.preset("square"))
		
		btnClr.grid(row=0, column=0)
		btnSquare.grid(row=0, column=1)
		
		#Sliders
			#Labels
		lblXcos = tk.Label(slider_frame, text="X - cos", font=LARGE_FONT)
		lblXsin = tk.Label(slider_frame, text="X - sin", font=LARGE_FONT)
		lblYcos = tk.Label(slider_frame, text="Y - cos", font=LARGE_FONT)
		lblYsin = tk.Label(slider_frame, text="Y - sin", font=LARGE_FONT)
		
		lblXcos.grid(row=0)
		lblXsin.grid(row=1)
		lblYcos.grid(row=2)
		lblYsin.grid(row=3)
			#Offsets
		for i in range(2):
			self.sliders_offset[i]=tk.Scale(slider_frame, from_=+self.extremum, to=-self.extremum, resolution=1, orient="vertical", command=self.update)
			self.sliders_offset[i].grid(row=2*i, column=1, rowspan=2)
			#Coefs
		for i in range(slider_nb):
			for j in range(4):
				self.sliders[j][i]=tk.Scale(slider_frame, from_=+self.extremum, to=-self.extremum, resolution=1, orient="vertical", command=self.update)
				self.sliders[j][i].grid(row=j, column=i+2)
	
	def preset(self, type):
		if type == "clear":
			prt = [ [0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0]]
		elif type == "square":
			prt = [ [1,0,-.26,0,.09],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[1,0,.24,0,.06]]
		
		for y,r in enumerate(prt):
			for x,v in enumerate(r):
				self.sliders[y][x].set(v*self.extremum)
		
		self.update()
	
	def update(self, evt=None):
		v=[[x.get()/self.extremum for x in y] for y in self.sliders]
		o=[x.get()/self.extremum for x in self.sliders_offset]
		
		for type in self.pages:
			if self.pages[type] is not None:
				self.pages[type].update(o, v)
	
	def new_graph_page(self, type, btn):
		handler = None
		if type in self.pages:
			handler = self.pages[type]
		
		if handler == None:
			self.newPage = tk.Toplevel(self.master)
			self.app = GraphPage(self.newPage, type)
			handler = self.app
			btn.configure(text="Close "+type)
		else:
			handler.master.destroy()
			handler = None;
			btn.configure(text="Open "+type)
		
		self.pages[type] = handler
		self.update()

		
		
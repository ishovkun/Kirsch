# coding: UTF-8
import sys
import pyqtgraph as pg
from PySide import QtCore, QtGui
import numpy as np
from Gradients import Gradients
from setupPlot import setup_plot

pg.setConfigOption('background', (255,255,255))
pg.setConfigOption('foreground',(0,0,0))

class ColorMapWidget(pg.GraphicsLayoutWidget):
	def __init__(self):
		super(ColorMapWidget,self).__init__(None,
		# QtCore.Qt.WindowStaysOnTopHint)
			)
		self.setupGUI()
	def setupGUI(self):
		self.setWindowTitle("Color Map Widget")
		# self.setGeometry(500, 300, 350, 200)
		self.plt = self.addPlot()
		setup_plot(self.plt)
		# self.plt.setLabel('left', yname)
		# self.plt.setLabel('bottom', xname)
		# self.img = pg.ImageItem()
		# self.plt.addItem(self.img)
		self.axis = pg.AxisItem('left')
		self.addItem(self.axis)
		self.gw = pg.GradientEditorItem(orientation='right')
		self.addItem(self.gw)

		GradiendMode = Gradients['hot']
		self.gw.restoreState(GradiendMode)


		def update():
			img = self.img.image
			lut = self.gw.getLookupTable(len(img), alpha=None)
			self.img.setLookupTable(lut, update=True)

		self.gw.sigGradientChanged.connect(update)

	def setImage(self,img,x=None,y=None,limits=None):
		self.img = pg.ImageItem()
		self.plt.addItem(self.img)
		self.img.setImage(img.T)
		self.axis.setRange(img.min(), img.max())
		lut = self.gw.getLookupTable(len(img), alpha=None)
		self.img.setLookupTable(lut, update=True)
		if limits:
			self.img.setLevels(limits)
			self.axis.setRange(min(limits), max(limits))
		if len(x) and len(y):
			x_width = x.max() - x.min()
			y_width = y.max() - y.min()			
			Nx = len(x)
			Ny = len(y)
			self.img.translate(x.min(),y.min())
			self.img.scale(x_width/Nx,y_width/Ny)

if __name__ == '__main__':
	App = QtGui.QApplication(sys.argv)
	w = ColorMapWidget()
	w.show()
	App.exec_()
# coding: UTF-8
import sys
import pyqtgraph as pg
from PySide import QtCore, QtGui
import numpy as np
import re
from lib.ColorMapWidget import ColorMapWidget
from lib.DataTreeWidget import DataTreeWidget
from lib.Stresser import Stresser

GoverningNames = ['S1','S2','BHP']
PlotNames = [u'σ_xx',u'σ_yy',u'σ_xy',u'σ_rr',u'σ_rθ']
S1Limits = [1e5,1e6]
S2Limits = [1e5,1e6]
BHPLimits = [1e5,1e6]
ColorLimits = [1e5,1e6]

class Widget(QtGui.QWidget):
	def __init__(self):
		super(Widget,self).__init__(None,
		# QtCore.Qt.WindowStaysOnTopHint)
			)
		self.setupGUI()
		self.tree.setLimits('S1',S1Limits)
		self.tree.setLimits('S2',S2Limits)
		self.tree.setLimits('BHP',BHPLimits)
		# self.tree.setStep('S1',MaxS1/100)
		# self.tree.setStep('S2',MaxS1/100)
		# self.tree.setStep('BHP',MaxS1/100)
		self.stresser = Stresser()
		self.stresser.setGeometry(1.,1.,0.1,200)
		self.stresser.setValues(6400,6300,6000)
		self.tree.checkBoxes['Plotting'][u'σ_rr'].setChecked(True)
		self.tree.valueChanged.connect(self.updateValues)
		self.tree.checkGroup.buttonClicked.connect(self.plot)
		self.plot()

		# self.tree.valueBoxes['Governing']
	def setupGUI(self):
		self.setWindowTitle("Kirsch Solution")
		# self.setGeometry(500, 300, 350, 200)
		self.layout = QtGui.QHBoxLayout()
		self.setLayout(self.layout)
		self.splitter = QtGui.QSplitter()
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		self.layout.addWidget(self.splitter)
		self.tree = DataTreeWidget()
		self.plt = ColorMapWidget()
		self.splitter.addWidget(self.tree)
		self.splitter.addWidget(self.plt)

		self.tree.addItems(GoverningNames,group='Governing')
		self.tree.addItems(PlotNames,group='Plotting')

		self.splitter.setSizes([int(self.width()*0.46),
								int(self.width()*0.54)])
		self.splitter.setStretchFactor(0, 0)
		self.splitter.setStretchFactor(1, 1)

	def updateValues(self):
		boxes = self.tree.valueBoxes['Governing']
		for item in boxes.keys():
			box = boxes[item]
			if item=='S1':
				S1 = box.value()
			elif item=='S2':
				S2 = box.value()
			elif item=='BHP':
				BHP = box.value()
		self.stresser.setValues(S1,S2,BHP)
		self.plot()
	def plot(self):
		active = self.tree.checkGroup.checkedButton()
		group,item = self.tree.findItem(active,self.tree.checkBoxes)
		if item == u'σ_rr':   img = self.stresser.Srr
		elif item == u'σ_rθ': img = self.stresser.Srt
		elif item == u'σ_θθ': img = self.stresser.Stt
		elif item == u'σ_xx': img = self.stresser.Sxx
		elif item == u'σ_yy': img = self.stresser.Syy
		elif item == u'σ_xy': img = self.stresser.Sxy
		self.plt.setImage(img,
			x=self.stresser.X[:,0],
			y=self.stresser.Y[0,:],
			limits=ColorLimits )
		self.plt.plt.autoRange()  


if __name__ == '__main__':
	App = QtGui.QApplication(sys.argv)
	w = Widget()
	w.show()
	App.exec_()
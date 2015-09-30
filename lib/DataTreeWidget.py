# -*- coding: utf-8 -*-
import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore, QtGui
from PySide import QtCore, QtGui
import numpy as np

class CheckBox(QtGui.QCheckBox):
	def __init__(self):
		super(CheckBox,self).__init__()
		self.name = None
	def value(self):
		state = self.checkState()
		if state == QtCore.Qt.CheckState.Unchecked:
			return False
		else: return True
	def setName(self,name):
		self.name = name

class DataTreeWidget(pg.TreeWidget):
	valueChanged = QtCore.Signal(object) # emitted when color changed
	def __init__(self,name=None,items=None,indent=5):
		super(DataTreeWidget,self).__init__()
		self.name = name
		ncolumns = 5
		self.setColumnCount(ncolumns)
		self.setHeaderHidden(True)
		self.setDragEnabled(False)
		self.header = pg.TreeWidgetItem([name])
		self.setIndentation(0)
		headerBackgroundColor = pg.mkBrush(color=(100,100,100))
		fontcolor = pg.mkBrush(color=(255,255,255))
		self.indent = indent
		self.setupHeader()
		self.items = {None:[]}
		self.sliders = {None:{}}
		self.valueBoxes = {None:{}}
		self.checkBoxes = {None:{}}
		self.limits = {None:{}}
		self.checkGroup = QtGui.QButtonGroup(self)
	def setupHeader(self):
		self.header = pg.TreeWidgetItem([self.name])
		self.setIndentation(0)
		headerBackgroundColor = pg.mkBrush(color=(100,100,100))
		fontcolor = pg.mkBrush(color=(255,255,255))
		self.header.setBackground(0,headerBackgroundColor)
		self.header.setBackground(1,headerBackgroundColor)
		self.header.setBackground(2,headerBackgroundColor)
		self.header.setBackground(3,headerBackgroundColor)
		self.header.setBackground(4,headerBackgroundColor)
		self.header.setForeground(0,fontcolor)
		self.addTopLevelItem(self.header)
		self.header.setSizeHint(0,QtCore.QSize(-1, 25))
		self.setColumnWidth (0, 100)
		self.setColumnWidth (1, 70)
		self.setColumnWidth (2, 10)
		self.setColumnWidth (3, 80)
		self.setColumnWidth (4, 1)
		self.setGeometry(100,100,290,600)
		

	def addItems(self,items,group=None):
		print 'Setting up tree'
		if group:
			subheader = pg.TreeWidgetItem([' '+group])
			self.header.addChild(subheader)
			self.items[group] = []
			if group=='Governing':
				self.sliders[group] = {}
				self.valueBoxes[group] = {}
				self.limits[group] = {}
			elif group=='Plotting':
				self.checkBoxes[group] = {}

		for item in sorted(items):
			child = pg.TreeWidgetItem([item])
			child.setText(0,' '*self.indent+item)
			self.header.addChild(child)
			self.items[group].append(item)
			
			if group == 'Governing':
				valueBox = pg.SpinBox(value=0, step=1)
				# print valueBox.__dict__
				# valueBox.opts['dec'] = True
				child.setWidget(1,valueBox)
				slider = QtGui.QSlider(orientation=QtCore.Qt.Horizontal)
				child.setWidget(3,slider)
				self.sliders[group][item] = slider
				self.valueBoxes[group][item] = valueBox
				self.limits[group][item] = [0.,99.]
				slider.valueChanged.connect(self.setValueBoxValue)
				valueBox.sigValueChanged.connect(self.setSliderPosition)
				valueBox.sigValueChanged.connect(self.emitValueChanged)

			elif group == 'Plotting':
				checkBox = QtGui.QRadioButton()
				self.checkGroup.addButton(checkBox)
				child.setWidget(1,checkBox)
				self.checkBoxes[group][item] = checkBox


		self.header.setExpanded(True)

	def findItem(self,item,controlGroup):
		'''
		returns item name and group
		'''
		for group in controlGroup.keys():
			if controlGroup[group] != {}:
				for itemName in controlGroup[group].keys():
					if controlGroup[group][itemName] == item:
						return [group,itemName]
			

	def setValueBoxValue(self):
		slider = self.sender()
		value = slider.value()
		group,item = self.findItem(slider,self.sliders)
		limits = self.limits[group][item]
		value = float(value)/99.*(limits[1]-limits[0])+limits[0]
		valueBox = self.valueBoxes[group][item]
		valueBox.setValue(value)


	def setSliderPosition(self):
		valueBox = self.sender()
		value = valueBox.value()
		group,item = self.findItem(valueBox,self.valueBoxes)
		limits = self.limits[group][item]
		value = int((value-limits[0])/(limits[1]-limits[0])*99)
		slider = self.sliders[group][item]
		# slider.valueChanged.disconnect(self.setValueBoxValue)
		slider.setValue(value)
		# slider.valueChanged.connect(self.setValueBoxValue)
		
	def emitValueChanged(self):
		self.valueChanged.emit(self)

	# def setLimits(self,itemName,limits):
	# 	slider = self.sliders['Governing'][itemName]
	# 	slider.setTickInterval(666)

	def setLimits(self,itemName,limits):
		self.limits['Governing'][itemName] = limits
		valueBox = self.valueBoxes['Governing'][itemName]
		if valueBox.value()<min(limits):
			valueBox.setValue(min(limits))
		elif valueBox.value()>max(limits):
			valueBox.setValue(max(limits))
	def setStep(self,itemName,step):
		valueBox = self.valueBoxes['Governing'][itemName]
		valueBox.opts['step'] = step

if __name__ == '__main__':
	names = ['chlen1','chlen2','chlen3']
	pnames = ['Sx','Sy','sigmaxx','Sigmaxy','Sigmayy']
	# col = [(255,0,0),(0,255,0),(0,0,255)]
	app = QtGui.QApplication([])
	
	tree = DataTreeWidget(name='Data')
	tree.addItems(names,group='Governing')
	tree.addItems(pnames,group='Plotting')
	tree.setLimits('chlen1',[1e8,1e9])
	tree.show()
	QtGui.QApplication.instance().exec_()
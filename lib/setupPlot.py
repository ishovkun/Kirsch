from PySide import QtGui



def setup_plot(plot,tickFontSize=12,tickOffset=8,axisWidth=70):
	'''
	input - pyqtgraph plot
	sets decent fonts for the plot
	tickFontSize - size of tick labels
	tickOffset - offset from axes to prevent overlapping with axis
	axisWidth = 70 # prevents text label from overlaping with ticks labels
	'''
	# font for tick labels
	tickFont = QtGui.QFont("Times", tickFontSize, QtGui.QFont.Bold)

	plot.getAxis('bottom').setStyle(tickTextOffset=tickOffset)
	plot.getAxis('bottom').tickFont = tickFont
	plot.getAxis('left').setStyle(tickTextOffset=tickOffset/2)
	plot.getAxis('left').setWidth(axisWidth)
	plot.getAxis('left').tickFont = tickFont
	plot.setXRange(1,2)
	plot.setYRange(1,2)
# coding: UTF-8
import sys
import numpy as np

class Stresser:
	S1 = None
	S2 = None
	S3 = None
	hasValues = False
	hasGeometry = False
	def setGeometry(self,xSize, ySize, Rwell, npoints=100):
		self.xSize = xSize
		self.ySize = ySize
		self.Rwell = Rwell
		self.N = npoints
		x = np.linspace(-xSize/2,xSize/2,npoints)
		y = np.linspace(-ySize/2,ySize/2,npoints)
		Y = np.ones((npoints,npoints))*y 
		X = np.transpose(np.ones((npoints,npoints))*x)
		theta = np.zeros((npoints,npoints))
		r = (X**2 + Y**2)**0.5
		pi = np.pi
		arccos = np.arccos
		theta[Y>=0] += arccos(X[Y>0]/r[Y>0])
		theta[Y<0]  += abs(arccos(X[Y<0]/r[Y<0]) - pi) + pi
		self.X = X
		self.Y = Y
		self.theta = theta
		self.r = r
		self.hasGeometry = True
		if self.hasValues:
			self.getPolarStresses()

	def setValues(self,S1,S2,BHP):
		self.S1 = S1
		self.S2 = S2
		self.BHP = BHP
		self.hasValues = True
		if self.hasGeometry:
			self.getPolarStresses()

	def getPolarStresses(self):
		S1 = self.S1; S2 = self.S2; BHP = self.BHP; R = self.Rwell
		r = self.r; theta = self.theta
		cos = np.cos; sin = np.sin
		self.Stt =   1./2*(S1 + S2)*(1. + (R/r)**2) \
		      - 1./2*(S1 - S2)*(1. + 3*(R/r)**4)*cos(2.*theta) - BHP*(R/r)**2
		self.Srr =   1./2*(S1 + S2)*(1.- (R/r)**2) + BHP*(R/r)**2 \
			  + 1./2*(S1 - S2)*(1. - 4*(R/r)**2 + 3.*(R/r)**4)*cos(2.*theta)
		self.Srt = - 1./2*(S1 - S2)*(1. + 2*(R/r)**2 - 3.*(R/r)**4)*sin(2.*theta)
		self.Stt[r<R] = self.Stt.mean()
		self.Srr[r<R] = self.Srr.mean()
		self.Srt[r<R] = self.Srt.mean()
		self.getCartesianStresses()

	def getCartesianStresses(self):
		cos = np.cos; sin = np.sin
		theta = self.theta
		Srr = self.Srr
		Stt = self.Stt
		Srt = self.Srt
		self.Sxx = cos(theta)**2*Srr + sin(theta)**2*Stt - sin(2*theta)*Srt
		self.Syy = sin(theta)**2*Srr + cos(theta)**2*Stt + sin(2*theta)*Srt
		self.Sxy = sin(2*theta)/2*Srr - sin(2*theta)/2*Stt + cos(2*theta)*Srt
		R = self.Rwell; r = self.r
		self.Sxx[r<R] = self.Sxx.mean()
		self.Sxy[r<R] = self.Sxy.mean()
		self.Syy[r<R] = self.Syy.mean()

	

if __name__ == '__main__':
	Str = Stresser()
	Str.setGeometry(100,100,100)
	Str.setValues(100,100,100)
	Str.getPolarStresses()

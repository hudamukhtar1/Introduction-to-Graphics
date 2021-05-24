# Name: Huda Mukhtar
# ID: hmukhta
# Student number: 251030469
# Date: February 18, 2021
# Purpose: This class generates a camera matrix
# Interpreter: Python 3.9
from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,window,UP,E,G,nearPlane=10.0,farPlane=50.0,theta=90.0):
        self.__UP = UP.normalize()
        self.__E = E
        self.__G = G
        self.__np = nearPlane
        self.__fp = farPlane
        self.__width = window.getWidth()
        self.__height = window.getHeight()
        self.__theta = theta
        self.__aspect = self.__width/self.__height
        self.__npHeight = self.__np*(pi/180.0*self.__theta/2.0)
        self.__npWidth = self.__npHeight*self.__aspect

        Mp = self.__setMp(self.__np,farPlane)
        T1 = self.__setT1(self.__np,self.__theta,self.__aspect)
        S1 = self.__setS1(self.__np,self.__theta,self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width,self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in the unit vectors: u,v,n and e, the location of the origin of the camera
    #          coordinate system. The created matrix is returned
    def __setMv(self,U,V,N,E):
        # Create the 4 by 4 identity matrix
        Mv = matrix(np.identity(4))
        # Fill up the matrix using the provided unit vectors based on the notes
        for uvector in range(3):
            if uvector == 0:
                unit = U
            elif uvector == 1:
                unit = V
            else:
                unit = N
            for column in range(4):
                if column != 3:
                    Mv.set(uvector, column, unit.get(column, 0))
                else: # The last row of the matrix does not depend on the unit vectors
                    Mv.set(uvector, 3, (-E.removeRow(3).transpose() * unit).get(0, 0))
        # Return the created matrix
        return Mv

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in the near plane and the far plane.
    #          The created matrix is returned
    def __setMp(self,nearPlane,farPlane):
        # Create the 4 by 4 identity matrix
        Mp = matrix(np.identity(4))
        # Calculate the value of a, b
        a = -(farPlane + nearPlane) / (farPlane - nearPlane)
        b = -2.0 * (farPlane * nearPlane) / (farPlane - nearPlane)
        # Set the values of the matrix based off of the notes
        Mp.set(0, 0, nearPlane)
        Mp.set(1, 1, nearPlane)
        Mp.set(2, 2, a)
        Mp.set(2, 3, b)
        Mp.set(3, 2, -1)
        # Return the created matrix
        return Mp

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in the near plane, theta, and aspect
    #          The created matrix is returned
    def __setT1(self,nearPlane,theta,aspect):
        # Create the 4 by 4 identity matrix
        T1 = matrix(np.identity(4))
        # Calculate the r, l, t, b as per the notes
        t = nearPlane * tan((pi / 180) * (theta / 2))
        r = aspect * t
        b = -1 * t
        l = -1 * r
        # Calculate the values for the matrix
        first = -1 * (r + l) / 2
        second = -1 * (t + b) / 2
        # Set the values of the matrix based off of the notes
        T1.set(0, 3, first)
        T1.set(1, 3, second)
        # Return the created matrix
        return T1

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in the near plane, theta, and aspect
    #          The created matrix is returned
    def __setS1(self,nearPlane,theta,aspect):
        # Create the 4 by 4 identity matrix
        S1 = matrix(np.identity(4))
        # Calculate the r, l, t, b as per the notes
        t = nearPlane * tan((pi / 180) * (theta / 2))
        r = aspect * t
        b = -1 * t
        l = -1 * r
        # Calculate the values for the matrix
        first = 2 / (r - l)
        second = 2 / (t - b)
        # Set the values of the matrix based off of the notes
        S1.set(0, 0, first)
        S1.set(1, 1, second)
        # Return the created matrix
        return S1

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in self and the created matrix is returned
    def __setT2(self):
        # Create the 4 by 4 identity matrix
        T2 = matrix(np.identity(4))
        # Set the values as defined by the notes
        T2.set(0, 3, 1)
        T2.set(1, 3, 1)
        # Return the created matrix
        return T2

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in self, width, and height and the created matrix is returned
    def __setS2(self,width,height):
        # Create the 4 by 4 identity matrix
        S2 = matrix(np.identity(4))
        # Calculate the values for the matrix
        first = width / 2
        second = height / 2
        # Set the values as defined by the notes
        S2.set(0, 0, first)
        S2.set(1, 1, second)
        # Return the created matrix
        return S2

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in height and the created matrix is returned
    def __setW2(self,height):
        # Create the 4 by 4 identity matrix
        W2 = matrix(np.identity(4))
        # Set the values as defined by the notes
        W2.set(1, 1, -1)
        W2.set(1, 3, height)
        # Return the created matrix
        return W2
        
    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getE(self):
        return self.__E

    def getG(self):
        return self.__G

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def getTheta(self):
        return self.__theta

    def getAspect(self):
        return self.__aspect

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getNpHeight(self):
        return self.__npHeight

    def getNpWidth(self):
        return self.__npWidth

    
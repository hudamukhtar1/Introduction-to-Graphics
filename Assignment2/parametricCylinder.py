# Name: Huda Mukhtar
# ID: hmukhta
# Student number: 251030469
# Date: February 18, 2021
# Purpose: This class generates a parametric cylinder
# Interpreter: Python 3.9
from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCylinder(parametricObject):

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The matrix, height, radius, color,
    # reflectance, ranges and differences of the unit vectors are taken in as parameters. The height and radius of
    # the cylinder are then initialized
    def __init__(self, T=matrix(np.identity(4)), height=1.0, radius=1.0, color=(0, 0, 0),
                 reflectance=(0.0, 0.0, 0.0, 0.0), uRange=(0.0, 0.0), vRange=(0.0, 0.0), uvDelta=(0.0, 0.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__height = height
        self.__radius = radius

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in the unit vectors: u,v. Then the location of the cylinder is created and returned
    def getPoint(self, u, v):
        P = matrix(np.ones((4, 1)))
        P.set(0, 0, self.__radius * sin(v))
        P.set(1, 0, self.__radius * cos(v))
        P.set(2, 0, self.__height * u)
        return P

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and height and sets the new height
    def setHeight(self, height):
        self.__height = height

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and returns the height
    def getHeight(self):
        return self.__height

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and radius and sets the new radius
    def setRadius(self, radius):
        self.__radius = radius

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and returns the radius
    def getRadius(self):
        return self.__radius

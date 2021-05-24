# Name: Huda Mukhtar
# ID: hmukhta
# Student number: 251030469
# Date: February 18, 2021
# Purpose: This class generates a parametric plane
# Interpreter: Python 3.9
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricPlane(parametricObject):
    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The matrix, height, width, color, reflectance, ranges and differences of the unit vectors are taken in as parameters.
    #          The width and height of the plane are then initialized
    def __init__(self, T=matrix(np.identity(4)), width=1.0, height=1.0, color=(0, 0, 0),
                 reflectance=(0.0, 0.0, 0.0, 0.0), uRange=(0.0, 0.0), vRange=(0.0, 0.0), uvDelta=(0.0, 0.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__width = width
        self.__height = height

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes in the unit vectors: u,v. Then the location of the plane is created and returned
    def getPoint(self, u, v):
        P = matrix(np.ones((4, 1)))
        first = u * self.__width
        second = v * self.__height
        P.set(0, 0, first)
        P.set(1, 0, second)
        P.set(2, 0, 0)
        return P

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and sets the height
    def setHeight(self, height):
        self.__height = height

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and height and sets the new height
    def getHeight(self):
        return self.__height

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and width sets the new width
    def setWidth(self, width):
        self.__width = width

    # Author: Huda Mukhtar
    # Date of creation: February 18, 2021
    # Purpose: The method takes self and returns the width
    def getWidth(self):
        return self.__width

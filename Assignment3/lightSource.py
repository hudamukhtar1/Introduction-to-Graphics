# Name: Huda Mukhtar
# ID: hmukhta
# Student number: 251030469
# Date: March 10, 2021
# Purpose: This class takes care of the light source with its getter and setter methods,
# that account for position, intensity, and color
# Interpreter: Python 3.9
import numpy as np
from matrix import matrix

class lightSource:

    def __init__(self,position=matrix(np.zeros((4,1))),color=(0,0,0),intensity=(1.0,1.0,1.0)):
        self.__position = position
        self.__color = color
        self.__intensity = intensity

    # Author: Huda Mukhtar
    # Date of creation: March 10, 2021
    # Purpose: The method takes in the self and returns the current position
    def getPosition(self):
        return self.__position;

    # Author: Huda Mukhtar
    # Date of creation: March 10, 2021
    # Purpose: The method takes in the self and returns the current color
    def getColor(self):
        return self.__color;

    # Author: Huda Mukhtar
    # Date of creation: March 10, 2021
    # Purpose: The method takes in the self and returns the intensity
    def getIntensity(self):
        return self.__intensity;

    # Author: Huda Mukhtar
    # Date of creation: March 10, 2021
    # Purpose: The method takes in the self, position and sets the new position
    def setPosition(self,position):
        self.__position = position;

    # Author: Huda Mukhtar
    # Date of creation: March 10, 2021
    # Purpose: The method takes in the self, color and sets the new color
    def setColor(self,color):
        self.__color = color;

    # Author: Huda Mukhtar
    # Date of creation: March 10, 2021
    # Purpose: The method takes in the self, intensity and sets the new intensity
    def setIntensity(self,intensity):
        self.__intensity = intensity;

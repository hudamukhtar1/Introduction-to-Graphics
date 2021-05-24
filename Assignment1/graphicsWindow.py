# Name: Huda Mukhtar
# ID: hmukhta
# Student number: 251030469
# Date: January 22, 2020
# Purpose: This class generates a window and uses the drawLine function to create lines on it
import operator
from PIL import Imae

class graphicsWindow:

    def __init__(self,width=640,height=480):
        self.__mode = 'RGB'
        self.__width = width
        self.__height = height
        self.__canvas = Image.new(self.__mode,(self.__width,self.__height))
        self.__image = self.__canvas.load()

    def drawPoint(self,point,color):
        if 0 <= point[0] < self.__width and 0 <= point[1] < self.__height:
            self.__image[point[0],point[1]] = color

    # Author: Huda Mukhtar
    # Date of creation: January 22, 2020
    # Purpose: The method takes in two points and its color and uses Bresenham's algorithm to draw a line using the
    #          drawPoint method in this class. There is no returned variable.
    def drawLine(self,point1,point2,color):

        # Declare variables of the points, initialize the length and height of the line by coordinates
        # as well as helper variable negative for calculations later
        x, y, firstChange, secondChange, negative = 0, 0, 1, 1, -1
        x1, y1 = int(point2.get(0, 0)) - int(point1.get(0, 0)), int(point2.get(1, 0)) - int(point1.get(1, 0))

        # calculate double the differences between the points for later calculations using Bresenham's algorithm
        twoDeltaX = (int(point2.get(0, 0)) - int(point1.get(0, 0))) * 2
        twoDeltaY = (int(point2.get(1, 0)) - int(point1.get(1, 0))) * 2

        # check to see whether the slope is increasing or decreasing, and whether the line is increasing or decreasing
        # if so, the delta calculations and slope changes are made negative accordingly
        if 0 > (int(point2.get(1, 0)) - int(point1.get(1, 0))):
            twoDeltaY = twoDeltaY * negative
            secondChange = negative
            y1 = y1 * negative
        if 0 > (int(point2.get(0, 0)) - int(point1.get(0, 0))):
            twoDeltaX = twoDeltaX * negative
            firstChange = negative
            x1 = x1 * negative

        # if the coordinates need to be reversed, use the swapped points, delta values and changes in Bresenham's algorithm to plot the line
        if x1 < y1:
            pi = twoDeltaX - y1
            for point in range(y1):
                if pi < 0:
                    pi = pi + twoDeltaX
                else:
                    pi = pi + twoDeltaX - twoDeltaY
                    y = y + firstChange
                x = x + secondChange
                self.drawPoint((y + int(point1.get(0, 0)), x + int(point1.get(1, 0))), color)
        # this is Bresenham's algorithm without the need to swap the coordinates
        else:
            pi = twoDeltaY - x1
            for point in range(x1):
                if pi < 0:
                    pi = pi + twoDeltaY
                else:
                    pi = pi + twoDeltaY - twoDeltaX
                    y = y + secondChange
                x = x + firstChange
                self.drawPoint((x + int(point1.get(0, 0)), y + int(point1.get(1, 0))), color)

    def saveImage(self,fileName):
        self.__canvas.save(fileName)

    def showImage(self):
        self.__canvas.show()

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height
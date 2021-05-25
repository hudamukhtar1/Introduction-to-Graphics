# Name: Huda Mukhtar
# ID: hmukhta
# Student number: 251030469
# Date: March 10, 2021
# Purpose: This class tessels the objects of the graphical scene into convex polygons, and computes the color shade to fill the polygons with, using lighting models.
# Interpreter: Python 3.9
import numpy as np
from matrix import matrix

class tessel:

    # Author: Huda Mukhtar
    # Student number: 251030469
    # Date: March 10, 2021
    # Purpose: This methods tessels the objects of the graphical scene into convex polygons, and computes the color shade to fill the polygons with, using lighting models.
    def __init__(self, objectList, camera, light):
        EPSILON = 0.001
        ZERO = 0
        ONE = 1
        # Create an empty list of faces. This is an instance variable for this class
        self.__faceList = []
        # Create an empty list for the points forming a face
        fPoints = []
        # Transform the position of the light into viewing coordinates (use method worldToViewingCoordinates from class cameraMatrix)
        lightPosInViewCoord = camera.worldToViewingCoordinates(light.getPosition())
        # Get light intensity values
        lightIntensity = light.getIntensity()
        # For each object in objectList:
        for object in objectList:
            # Get the object color
            objColor = object.getColor()
            uRange = object.getURange()[ZERO]
            # While u + the delta u of the object is smaller than the final value of the u-parameter range + EPSILON:
            cond = uRange + object.getUVDelta()[ZERO] < object.getURange()[ONE] + EPSILON
            while cond:
                # u becomes the start value of the u-parameter range for the object
                # v become the start value of the v-parameter range for the object
                vRange = object.getVRange()[ZERO]
                # While v + the delta v of the object is smaller than the final value of the v-parameter range + EPSILON:
                secCond = vRange + object.getUVDelta()[ONE] < object.getVRange()[ONE] + EPSILON
                # Collect surface points transformed into viewing coordinates in the following way:
                while secCond:
                    # Get object point at (u,v), (u, v + delta v), (u + delta u, v + delta v), and (u + delta u, v)
                    # Transform these points with the transformation matrix of the object
                    # Transform these points from world to viewing coordinates
                    # Append these points (respecting the order) to the list of face points
                    point1 = camera.worldToViewingCoordinates(object.getT() * object.getPoint(uRange, vRange))
                    point2 = camera.worldToViewingCoordinates(object.getT() * object.getPoint(uRange, vRange + object.getUVDelta()[ONE]))
                    point3 = camera.worldToViewingCoordinates(object.getT() * object.getPoint(uRange + object.getUVDelta()[ZERO], vRange + object.getUVDelta()[ONE]))
                    point4 = camera.worldToViewingCoordinates(object.getT() * object.getPoint(uRange + object.getUVDelta()[ZERO], vRange))
                    fPoints.append(point1)
                    fPoints.append(point2)
                    fPoints.append(point3)
                    fPoints.append(point4)
                    # Make sure we don't render any face with one or more points behind the near plane in the following way:
                    # If this minimum Z-value is not greater than -(Near Plane) (so the face is not behind the near plane):
                    if not -1*camera.getNp() < self.__minCoordinate(fPoints, 2):
                        # Compute the minimum Z-coordinate from the face points
                        centroidPoint = self.__centroid(fPoints)  # Compute the centroid point of the face points
                        normVector = self.__vectorNormal(fPoints)  # Compute the normal vector of the face, normalized
                        # Compute face shading, excluding back faces (normal vector pointing away from camera) in the following way:
                        if not self.__backFace(centroidPoint, normVector):
                            # S is the vector from face centroid to light source, normalized
                            S = self.__vectorToLightSource(lightPosInViewCoord, centroidPoint)
                            # R is the vector of specular reflection
                            R = self.__vectorSpecular(S, normVector)
                            # V is the vector from the face centroid to the origin of viewing coordinates
                            V = self.__vectorToEye(centroidPoint)
                            # Compute color index
                            index = self.__colorIndex(object, normVector, S, R, V)
                            # Obtain face color (in the RGB 3-color channels, integer values) as a tuple:
                            # (object color (red channel) * light intensity (red channel) * index,
                            rChannel = (objColor[ZERO] * lightIntensity[ZERO] * index)
                            # object color (green channel) * light intensity (green channel) * index,
                            gChannel = (objColor[ONE] * lightIntensity[ONE] * index)
                            # object color (blue channel) * light intensity (blue channel) * index)
                            bChannel = (objColor[2] * lightIntensity[2] * index)
                            faceColor = (int(rChannel), int(gChannel), int(bChannel))
                            # For each face point:
                            # Transform point into 2D pixel coordinates and append to a pixel face point list
                            pFPoints = []
                            for x in fPoints:
                                # Add all face attributes to the list of faces in the following manner:
                                # transform the face centroid from viewing to pixel coordinates
                                transformedPCoord = camera.viewingToPixelCoordinates(x)
                                pFPoints.append(transformedPCoord)
                            # append pixel Z-coordinate of face centroid, the pixel face point list, and the face color
                            self.__faceList.append((camera.viewingToPixelCoordinates(centroidPoint).get(2, 0), pFPoints, faceColor))
                    # Re-initialize the list of face points to empty
                    fPoints = []
                    # v become v + delta v
                    vRange += object.getUVDelta()[ONE]
                # u becomes u + delta u
                uRange += object.getUVDelta()[ZERO]

    def __minCoordinate(self, facePoints, coord):
        # Computes the minimum X, Y, or Z coordinate from a list of 3D points
        # Coord = 0 indicates minimum X coord, 1 indicates minimum Y coord, 2 indicates minimum Z coord.
        min = facePoints[0].get(coord, 0)
        for point in facePoints:
            if point.get(coord, 0) < min:
                min = point.get(coord, 0)
        return min

    def __backFace(self, C, N):
        # Computes if a face is a back face with using the dot product of the face centroid with the face normal vector
        return C.dotProduct(N) > 0.0

    def __centroid(self, facePoints):
        # Computes the centroid point of a face by averaging the points of the face
        sum = matrix(np.zeros((4, 1)))
        for point in facePoints:
            sum += point
        return sum.scalarMultiply(1.0 / float(len(facePoints)))

    def __vectorNormal(self, facePoints):
        # Computes the normalized vector normal to a face with the cross product
        U = (facePoints[3] - facePoints[1]).removeRow(3).normalize()
        V = (facePoints[2] - facePoints[0]).removeRow(3).normalize()
        return U.crossProduct(V).normalize().insertRow(3, 0.0)

    def __vectorToLightSource(self, L, C):
        return (L.removeRow(3) - C.removeRow(3)).normalize().insertRow(3, 0.0)

    def __vectorSpecular(self, S, N):
        return S.scalarMultiply(-1.0) + N.scalarMultiply(2.0 * (S.dotProduct(N)))

    def __vectorToEye(self, C):
        return C.removeRow(3).scalarMultiply(-1.0).normalize().insertRow(3, 0.0)

    def __colorIndex(self, object, N, S, R, V):
        # Computes local components of shading
        Id = max(N.dotProduct(S), 0.0)
        Is = max(R.dotProduct(V), 0.0)
        r = object.getReflectance()
        index = r[0] + r[1] * Id + r[2] * Is ** r[3]
        return index

    def getFaceList(self):
        return self.__faceList

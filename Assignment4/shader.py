# Name: Huda Mukhtar
# ID: hmukhta
# Student number: 251030469
# Date: April 9, 2021
# Purpose: This class uses ray tracing algorithms to implement lighting models for shadows on objects
class shader:

    # Author: Huda Mukhtar
    # Student number: 251030469
    # Date: April 9, 2021
    # Purpose: This method takes the object, list of object, an intersection and a light vector as its parameters
    # The method true if the ray from the intersection point to the light source intersects with an object from the scene
    #  and returns false otherwise
    def __shadowed(self,object,I,S,objectList):
        # M = matrix T associated with object
        M = object.getT()
        # detach the intersection point from its surface, and then transforms it into world coordinates
        I = M * (I + S.scalarMultiply(0.001))
        # transforms S into world coordinates
        S = M * S
        for obj in objectList:
            #  inverse of matrix T associated with object
            M_Inverse = obj.getT().inverse()  
            # transforms the intersection point into the generic coordinates of the object
            I2 = M_Inverse * I
            # transforms the vector to the light source into the generic coordinates of the object
            S2 = (M_Inverse * M * S).normalize()
            # if an intersection exists
            if object.intersection(I2,S2) != -1.0:    
                return True
        # otherwise return false
        return False    

    # Author: Huda Mukhtar
    # Student number: 251030469
    # Date: April 9, 2021
    # Purpose: This method takes the intersection, list of objects, camera matrix, ray, and a light vector as its parameters
    # This method determines the color for the pixel using the input parameters
    def __init__(self,intersection,direction,camera,objectList,light):
        # consider tuple (k ,t0) from intersection
        k, t0 = intersection    
        # object = objectList [k ]
        object = objectList[k]
        # M−1 = inverse of matrix T associated with object
        M_Inverse = object.getT().inverse()
        # T s = light position transformed with M−1
        t_s = M_Inverse * light.getPosition()    
        # transform the ray with M−1 in the following way: T e=M−1e , where e is the position of the camera
        t_e = M_Inverse * camera.getE()           
        # and T d=M−1 d , where d is the direction of the ray
        t_d = M_Inverse * direction              
        # compute the intersection point as I=T e+T dt0
        I = t_e + (t_d.scalarMultiply(t0))  
        # compute vector from intersection point to light source position as S=(T s−I) , and normalize it      
        S = (t_s - I).normalize()     
        # compute normal vector at intersection point as N = object.normalVector (I )      
        N = object.normalVector(I)              
        # compute specular reflection vector as R=−S+(2 S⋅N )N
        R = -S + N.scalarMultiply((S.scalarMultiply(2)).dotProduct(N))  
        # • compute vector to center of projection V =T e−I , and normalize it
        V = (t_e - I).normalize()     
        # compute I d=max {N⋅S ,0} and I s=max {R⋅V ,0} (different light intensities)          
        i_d = max((N.dotProduct(S)), 0)       
        i_s = max((R.dotProduct(V)), 0)       
        # get object reflectance, color, and intensity
        r = object.getReflectance()
        c = object.getColor()
        l_i = light.getIntensity()
        # if the intersection point is not shadowed by other objects 
        if (self.__shadowed(object, I, S, objectList) == False):
            # calculate the lighting accordingly
            f = r[0] + r[1] * i_d + r[2] * (i_s ** r[3])                                           
        else:
            # otherwise, just use the reflectance
            f = r[0]                                          
        originalColor = (c[0] * l_i[0], c[1] * l_i[1], c[2] * l_i[2])
        # use the calculated lighting on our object
        first = int(f * originalColor[0])
        second = int(f * originalColor[1])
        third = int(f * originalColor[2])
        self.__color = (first, second, third)

    def getShade(self):
        return self.__color
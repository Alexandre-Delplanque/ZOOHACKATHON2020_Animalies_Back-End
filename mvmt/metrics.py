import math

class mvmtMetrics(object):

    def __init__(self, points):
        self.points = points 

    @property
    def distances(self):
        '''
        Return distances between points.
        '''

        # Radius of earth in km
        R = 6378.137

        distances = []
        for (x1 , y1) , (x2 , y2) in zip(self.points[::1],self.points[1::1]):
            
            # Haversine formula
            d_long = x2 * math.pi / 180 - x1 * math.pi / 180
            d_lat = y2 * math.pi / 180 - y1 * math.pi / 180

            a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
                math.cos(x1 * math.pi / 180) * math.cos(x2 * math.pi / 180) * \
                math.sin(d_long/2) * math.sin(d_long/2)
            
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

            d = R * c * 1000

            distances.append(d)
        
        return distances
    
    @property
    def AbsoluteAngles(self):
        '''
        Return absolute angles between vectors.
        '''
        
        p = self.points

        angles = []
        for i , (x1 , y1) in zip(range(len(p)),p):

            if i>0:
                x_rel = x1-p[i-1][0]
                y_rel = y1-p[i-1][1]
                angle = math.degrees(math.atan(y_rel / x_rel))

                angles.append(angle)

        return angles

    @property
    def TurningAngles(self):
        '''
        Return relative (turning) angles between vectors.
        '''

        p = self.points

        angles = []
        for i , (x1 , y1) , (x2 , y2) in zip(range(len(p)),p[::1],p[1::1]):

            if i>0:
                dot = ((x1-p[i-1][0])*(x2-x1)) + ((y1-p[i-1][1])*(y2-y1))
                mod_1 = math.sqrt((x1-p[i-1][0])**2 + (y1-p[i-1][1])**2)
                mod_2 = math.sqrt((x2-x1)**2 + (y2-y1)**2)

                if mod_1 != 0 and mod_2 != 0:
                    angle = math.degrees(math.acos(dot / (mod_1 * mod_2)))
                else:
                    angle = 0

                angles.append(angle)

        return angles
    
    @property
    def SquaredNetDisplacement(self):
        '''
        Return the squared net displacement, which is
        the squared distance between first and last points.
        '''

        p = self.points

        x1 , y1, x2 , y2 = p[0][0] , p[0][1] , p[-1][0] , p[-1][1]

        # Radius of earth in km
        R = 6378.137

        # Haversine formula
        d_long = x2 * math.pi / 180 - x1 * math.pi / 180
        d_lat = y2 * math.pi / 180 - y1 * math.pi / 180

        a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
            math.cos(x1 * math.pi / 180) * math.cos(x2 * math.pi / 180) * \
            math.sin(d_long/2) * math.sin(d_long/2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = R * c * 1000

        return d**2
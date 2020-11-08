import math
import datetime
import shapefile

def distance(lat1, lon1, lat2, lon2):
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # meters

class Position(object):
    def __init__(latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class AnimalPosition(object):
    def __init__(self, record):
        self.record = record
    
    @property
    def timestamp(self):
        return datetime.datetime.strptime(self.record["timestamp"], '%Y-%m-%d %H:%M:%S.%f')

    @property
    def longitude(self):
        return self.record['location-l']

    @property
    def latitude(self):
        return self.record['location_1']
    
    @property
    def id(self):
        return self.record['individu_1']

    def __str__(self):
        return f"{self.id} - {self.timestamp} - {self.longitude},{self.latitude}"
    
    def to_dict(self):
        return {
            "id" : self.id,
            "latitude" : self.latitude,
            "longitude" : self.longitude
        }

class DataFilter(object):
    def filter_dataset(dataset):
        """Return a list of AnimalPositions that satisfy the filter.
        
        Subclasses must override this method to define how to filter data.
        """
        pass

class TimeWindow(DataFilter):
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
    
    def filter_dataset(self, dataset):
        return FilteredDataset([ \
            p for p in dataset.animal_positions \
            if self.start_time <= p.timestamp and p.timestamp <= self.end_time ])

class PositionArea(DataFilter):
    def __init__(self, center_position, border_position):
        self.center_position = center_position
        self.border_position = border_position
    
    @property
    def radius(self):
        return distance(
            self.center_position.latitude,
            self.center_position.longitude,
            self.border_position.latitude,
            self.border_position.longitude
        )
    
    def is_in_area(self, position):
        return distance(
            self.center_position.latitude,
            self.center_position.longitude,
            position.latitude,
            position.longitude) > self.radius
    
    def filter_dataset(self, dataset):
        return FilteredDataset([ \
            p for p in dataset.animal_positions \
            if self.is_in_area(p) ])
    
class IdDataFilter(DataFilter):
    def __init__(self, id):
        self.id = id
    
    def filter_dataset(self, dataset):
        return FilteredDataset([ \
            p for p in dataset.animal_positions \
            if p.id == self.id])

class Area(object):
    def __init__(self, border_positions):
        self.border_positions = border_positions
    
    def filter_dataset(self, dataset):
        #TODO
        pass

class AreaAnimalsCanNotGoOut(Area):
    pass

class AreaAnimalsCanNotGoIn(Area):
    pass

class AnimalsInIllegalZone(DataFilter):
    def filter_dataset(self, dataset):
        #TODO
        pass

class DataSet(object):
    @property
    def animal_positions(self):
        """Return the list of animal positions.

        To be overriden in subclasses.
        """
        pass
    
    def filter(self, data_filter):
        return data_filter.filter_dataset(self)
    
    def __iter__(self):
        for a in self.animal_positions:
            yield a

class DataSetFromShapeFile(DataSet):
    def __init__(self, animal_positions_shape_file_path, areas_shape_files_paths):
        self.animal_positions_shape_file = shapefile.Reader(animal_positions_shape_file_path)
        self.areas_shape_files = [shapefile.Reader(f) for f in areas_shape_files_paths]
    
    @property
    def animal_positions(self):
        return [ AnimalPosition(record) for record in self.animal_positions_shape_file.records() ]

class FilteredDataset(DataSet):
    def __init__(self, animal_positions):
        self._animal_positions = animal_positions
    
    @property
    def animal_positions(self):
        return self._animal_positions
    
if __name__ == "__main__":
    m = DataSetFromShapeFile("/home/julien/Documents/ZooHackathon/etosha_15_elephant_3857/etosha_15_elephants_EPSG3857", [])
    print(m.animal_positions[0].timestamp)
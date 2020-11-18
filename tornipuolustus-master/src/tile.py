from coordinates import Coordinates
from tower import Tower

class Tile():
    '''
    class that represents a single tile in the game. initialized with two int parameters that are the tile's coordinates
    '''
    def __init__(self, x, y):
        # set the coordinates
        self.coordinates = Coordinates(x, y)
        # init the type as basic first
        self.type = "Basic"
        self.hasTower = False
        
    def get_coordinates(self):
        # return the coordinates of the tile (Coordinates)
        return self.coordinates
    
    def set_type(self, typeinit):
        # set the type of the tile, takes one int parameter
        if typeinit == 1:
            self.type = "Road"
			
        if typeinit == 2:
            self.type = "Tower"
        
        if typeinit == 3:
            self.type = "Start"
        
        if typeinit == 4:
            self.type = "End"
            
    def get_type(self):
        # return the type of the tile (str)
        return self.type
    
    def set_tower(self):
        # set a tower to the tile, return True if succesful, else return False (the tile already has a tower in it)
        if self.hasTower == False:
            self.tower = Tower(self.coordinates.get_x(), self.coordinates.get_y())
            self.hasTower = True
            return True
        else:
            return False
    
    def get_tower(self):
        # return the tile's tower (Tower)
        if self.hasTower == True:
            return self.tower

class Coordinates():
    '''
    simple coordinate class that is used with the tile system, takes two int parameters
    '''
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        
    def get_x(self):
        # return the x coordinate
        return self.x
    
    def get_y(self):
        # return the y coordinate
        return self.y
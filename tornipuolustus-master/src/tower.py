from coordinates import Coordinates
from PyQt5.QtCore import QTimer

class Tower():
    '''
    class that represents a single tower in the game. initialized with two int parameters that are the tower's x and y coordinates.
    '''
    def __init__(self, x, y):
        # set the tower's coordinates
        self.coordinates = Coordinates(x, y)
        # set damage
        self.damage = 50
        # set range in pixels
        self.range = 90
        # init target identification and shoot status
        self.target_id = None
        self.has_target = False
        self.shoot_status = False
        # a timer that adds cooldown (1 second) to the shooting interval of the tower
        self.timer = QTimer()
        self.timer.timeout.connect(self.can_shoot)
        self.timer.start(1000)
        
    def get_range(self):
        # return the range of the tower (int)
        return self.range
        
    def set_target(self, id):
        # whenever a tower finds an enemy in its range set it as the towers current target. takes one int parameter that is saved 
        # and used in finding the correct target unit during every update
        self.has_target = True
        self.target_id = id
        
    def delete_target(self):
        # called when the tower's target dies, enables the tower to find a new target
        self.has_target = False
        self.target_id = None
        
    def get_target_status(self):
        # return the target status of the tower: True if the tower has target, else False (bool)
        return self.has_target
        
    def get_x_coord(self):
        # return the x coordinate of the tower (int)
        return self.coordinates.get_x()
        
    def get_y_coord(self):
        # return the y coordinate of the tower (int)
        return self.coordinates.get_y()
    
    def get_dmg(self):
        # return the damage of the tower (int)
        return self.damage
    
    def get_target_id(self):
        # return the tower's current target's id (int)
        return self.target_id
        
    def can_shoot(self):
        # called a second after the tower has shot, enables the tower to shoot again
        self.shoot_status = True
    
    def get_shoot_status(self):
        # return the shoot status of the tower, if it can fire return True, else False is returned (bool)
        return self.shoot_status
    
    def shot(self):
        # called after every shot, sets self.shoot_status to False and starts the timer that calls can_shoot after 1 second
        self.shoot_status = False
        self.timer.start(1000)
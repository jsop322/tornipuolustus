
from coordinates import Coordinates
from PyQt5 import QtWidgets, QtGui, QtCore

class Enemy(QtWidgets.QGraphicsEllipseItem):
    '''
    class that represents the enemy units. takes 4 int parameters: x and y for origin placement and
    sizex and sizey for the size of the ellipse item
    '''

    # init the id number that is used in targeting
    next_id = 0
    # init the hp value that is used in increasing the difficulty, increased every 20 seconds in tower_defence.py
    hp_base = 0
    
    def __init__(self, x, y , sizex, sizey):
        
        # init the parent object
        super(Enemy, self).__init__()
        
        #add id to the unit
        self.id = Enemy.next_id
        #increase id number for the next unit
        Enemy.next_id += 1
        
        self.x = x
        self.y = y
        # init the last tile the unit was standing on
        self.last_tile = Coordinates(int(x/30), int(y/30))
        # set shape and color
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        self.setRect(self.x, self.y, sizex, sizey)
        self.setBrush(QtGui.QColor(255, 0, 0))
        
        # init other stuff
        self.direction = None
        self.tile_changed = False
        self.walk_counter = 0
        self.health = None
        self.speed = None
        self.bounty = None
        self.score_value = None

    def set_pos(self, x, y):
        # takes two int parameters, sets the position of the object in pixel coordinates
        self.x = x
        self.y = y
        self.setPos(x, y)
        
    def get_x_pos(self):
        # return the x position (float)
        return self.x
    
    def get_y_pos(self):
        # return the y position (float)
        return self.y
        
    def set_last_tile(self, coordinates):
        # when the unit changes tiles this method is called. saves the previous tile's coordinates
        self.last_tile = coordinates
        
    def get_last_tile(self):
        # returns the coordinates of the last tile (Coordinates)
        return self.last_tile

        
    def set_dir(self, dirinit):
        
        # used in path finding in tower_defence.py, takes one int parameter
        
        if dirinit == 1:
            self.direction = "up"
			
        if dirinit == 2:
            self.direction = "down"
        
        if dirinit == 3:
            self.direction = "right"
        
        if dirinit == 4:
            self.direction = "left"
     
    def get_dir(self):
        # returns the current direction the unit is moving in (str)
        return self.direction
    
    def get_changed_tile(self):
        # returns True if the unit changed tiles, otherwise False
        return self.tile_changed
        
    def tile_change(self):
        # called when the unit changes tiles
        self.tile_changed = True
    
    def set_tile_changed_false(self):
        # called if the units previous location was in the same tile
        self.tile_changed = False
    
    def get_counter(self):
        # returns the count (int) of the units walk counter that is used to assure that the unit walks in the middle of the path
        return self.walk_counter
        
    def reset_counter(self):
        # resets the walk counter
        self.walk_counter = 0
        
    def hurt(self, dmg):
        # damages the unit, takes one int parameter that is subtracted from the units health points
        self.health -= dmg
        
    def get_id(self):
        # returns the id number of the unit (int)
        return self.id
        
    def get_health(self):
        # returns the health points of the unit (int)
        return self.health
        
    def get_speed(self):
        #returns the speed of the unit (int)
        return self.speed
    
    def get_bounty(self):
        # returns the gold bounty of the unit (int)
        return self.bounty
    
    def get_score_value(self):
        # returns the score value of the unit (int)
        return self.score_value

    '''
    below are subclasses for different enemytypes. at the moment only different hp, speed, score and bounty values are used.
    '''
        
class BasicEnemy(Enemy):
    
    def __init__(self):
        # init the parent object
        super(BasicEnemy, self).__init__(-5, -5, 10, 10)
        self.speed = 1
        self.health = 100 + Enemy.hp_base
        self.bounty = 10
        self.score_value = 100
        
        
    def increase_counter(self):
        self.walk_counter += self.speed
        
class BigEnemy(Enemy):
    
    def __init__(self):
        # init the parent object
        super(BigEnemy, self).__init__(-10, -10, 20, 20)
        self.speed = 0.5
        self.health = 200 + Enemy.hp_base
        self.bounty = 15
        self.score_value = 200
        
    def increase_counter(self):
        self.walk_counter += self.speed
        
class FastEnemy(Enemy):
    
    def __init__(self):
        # init the parent object
        super(FastEnemy, self).__init__(-5, -5, 10, 10)
        self.speed = 2.5
        self.health = 50 + Enemy.hp_base
        self.bounty = 20
        self.score_value = 50
        
    def increase_counter(self):
        self.walk_counter += self.speed

   
   
    
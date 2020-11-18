
from coordinates import Coordinates
from PyQt5 import QtWidgets, QtGui, QtCore

class Projectile(QtWidgets.QGraphicsEllipseItem):
    '''
    class that represents the projectiles that the towers are firing. very similiar to the enemy class as they both are QGraphicsEllipseItems.
    takes 4 parameters: x and y for origin placement and sizex and sizey for the size of the ellipse item
    '''
    def __init__(self, x, y, sizex, sizey):
        # init the parent object
        super(Projectile, self).__init__()
        self.x = x
        self.y = y
        # set shape and color
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        self.setRect(self.x, self.y, sizex, sizey)
        self.setBrush(QtGui.QColor(0, 0, 0))
        # init speed of the projectile
        self.speed = 30
     
    def set_pos(self, x, y):
        # takes two int parameters, sets the position of the object in pixel coordinates
        self.x = x
        self.y = y
        self.setPos(x, y)
        
    def get_x_pos(self):
        # return the x position (int)
        return self.x
    
    def get_y_pos(self):
        # return the y position (int)
        return self.y

    def set_target_x(self, x):
        # set the target x location in pixel coordinates, takes one int parameter
        self.target_x = x
        
    def set_target_y(self, y):
        # set the target y location in pixel coordinates, takes one int parameter
        self.target_y = y
        
    def get_target_x(self):
        # return the x target location (int)
        return self.target_x
        
    def get_target_y(self):
        # return the x target location (int)
        return self.target_y
        
    def get_speed(self):
        # return the speed value (int)
        return self.speed
    
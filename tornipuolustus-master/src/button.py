from PyQt5 import QtWidgets, QtGui, QtCore

class Button(QtWidgets.QGraphicsPolygonItem):
    
    
    def __init__(self, x, y, r, g, b):
        # create a button using the given parameters, x and y are for size, r, g and b for color
        super(Button, self).__init__()
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.pressed = False
        self.constructSquareVertices()
        
    def constructSquareVertices(self):

        # create a new QPolygon object
        square = QtGui.QPolygonF()

        # add the corners of a square to the the polygon object
        square.append(QtCore.QPointF(0, 0)) # top left
        square.append(QtCore.QPointF(self.x, 0)) # top right
        square.append(QtCore.QPointF(self.x, self.y)) # bottom right
        square.append(QtCore.QPointF(0, self.y)) # bottom left
        square.append(QtCore.QPointF(0, 0)) # top left

        # set this created polygon as this item's polygon
        self.setPolygon(square)
        #  set the color
        self.setBrush(QtGui.QColor(self.r, self.g, self.b))

    def mousePressEvent(self, *args, **kwargs):
        '''
        if mouse is pressed over the button the bool value of press status is changed 
        and the color of the button is changed a bit darker to indicate the press
        '''
        
        self.pressed = True
        self.setBrush(QtGui.QColor(self.r - 40, self.g - 40, self.b - 40))
    
    def getStatus(self):
        # returns the bool value of pressed status
        return self.pressed
    
    def setFalse(self):
        # sets pressed status to false and resets the color
        self.pressed = False
        self.setBrush(QtGui.QColor(self.r, self.g, self.b))
        

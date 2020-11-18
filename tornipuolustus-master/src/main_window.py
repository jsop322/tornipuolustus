from tower_defence import TowerDefence
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsView, QWidget)
from PyQt5.QtCore import Qt


class MainWindow(QGraphicsView):
    def __init__(self):
        # init the parent object
        super(MainWindow, self).__init__()
        # set window to fixed size, both values are bit over 600 to get rid of annoying sliders that show up
        # if they are set to 600
        self.setFixedSize(603, 602)
        # create a scene for the window
        self.scene = QGraphicsScene(self)
        # set the title of the window
        self.setWindowTitle('Tower Defence')
        # init the game, pass the created scene
        self.towerdefence = TowerDefence(self.scene)
        # add the game to the scene
        self.scene.addItem(self.towerdefence)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.setScene(self.scene)
        self.show()
        
    
    def keyPressEvent(self, event):
        # resets the game to main menu state if R is pressed at any time
        if event.key() == Qt.Key_R:
            self.scene.clear()
            self.towerdefence = TowerDefence(self.scene)
            self.scene.addItem(self.towerdefence)

    def update(self):
        # currently useless, might be needed in future
        pass
        
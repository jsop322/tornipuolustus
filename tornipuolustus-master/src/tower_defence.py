from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene, QTextBrowser,
                             QGraphicsView, QGraphicsTextItem, QGraphicsRectItem)
from button import Button
from game_world import GameWorld
from tile import Tile
from enemy import Enemy, BasicEnemy, BigEnemy, FastEnemy
from coordinates import Coordinates
from projectile import Projectile
import math
from corrupted_file_error import *

class TowerDefence(QGraphicsItem):
    '''
    The game class that handles most of the user inputs, creates and updates the game
    '''
    def __init__(self, scene):
    
        # init the parent object
        super(TowerDefence, self).__init__()
        # init font for text items
        self.font = QFont("Times", 25, QFont.Bold)
        self.bfont = QFont("Times", 20)
        # init the size of tiles in pixels
        self.tile_size = 30
        # set the base hp value that is added to the enemies hp. starts at 0 and is increased by 20 every 20 seconds
        Enemy.hp_base = 0
        # while in main menu the playing status is False
        self.playing = False
        # bool value that is used in the painter method
        self.painted = False
        # QGraphicsScene from the MainWindow class
        self.scene = scene
        # init the game world
        self.game = GameWorld()
        

        # init main menu buttons
        self.startbutton = Button(300, 50, 0, 102, 204)
        self.startbutton.setPos(150, 200)
        self.quitbutton = Button(300, 50, 0, 102, 204)
        self.quitbutton.setPos(150, 300)
        
        # init title text and text over buttons
        self.text1 = QGraphicsTextItem()
        self.text1.setPos(220, 205)
        self.text1.setFont(self.bfont)
        self.text1.setPlainText("START GAME")
        
        self.text2 = QGraphicsTextItem()
        self.text2.setPos(267, 303)
        self.text2.setFont(self.bfont)
        self.text2.setPlainText("QUIT")
        
        self.titletext = QGraphicsTextItem()
        self.titletext.setPos(174, 100)
        self.titletext.setFont(self.font)
        self.titletext.setPlainText("Tower Defence")
        
        # add the buttons and title to the scene
        self.scene.addItem(self.startbutton)
        self.scene.addItem(self.quitbutton)
        self.scene.addItem(self.text1)
        self.scene.addItem(self.text2)
        self.scene.addItem(self.titletext)
        
        # timer that is used in calling the spawn_enemy method every 1.5 seconds
        self.enemytimer = QTimer()
        self.enemytimer.timeout.connect(self.spawn_enemy)
        self.enemytimer.start(1500)
        
        # timer that calls the update_game method every 20 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)
        
        # timer that calls the clear status method, the timer is started every time a status message is shown
        self.statustimer = QTimer()
        self.statustimer.timeout.connect(self.clear_status)
        
        # timer that calls the update_difficulty method every 20 seconds (increases enemy hp)
        self.difficulty = QTimer()
        self.difficulty.timeout.connect(self.update_difficulty)
        self.difficulty.start(20000)
        self.enemy_counter = 0
        
        # init other stuff
        self.player_gold = 100
        self.score = 0
        self.end = False
        
        self.enemies = []
        self.towers = []
        self.projectiles = []

        # init the self.status_message QGraphicsTextItem that is used in storing and showing the current status message
        self.status_message = QGraphicsTextItem()
        self.status_message.setPos(420, 510)
        self.status_message.setPlainText("")
        self.scene.addItem(self.status_message)
        
    def boundingRect(self):
        # init the bounding rectangle
        return QRectF(0,0,600,600)
    
    def update_game(self):
        # call the update methods
        self.update_enemy()
        self.update_towers()
        self.update_projectiles()
        
    def update_difficulty(self):
        # updates the enemy hp by 50 every 20 seconds, called by self.difficulty timer
        Enemy.hp_base += 50
    
    def update_enemy(self):
        
        # updates the enemy objects. called every 20ms by self.timer
        
        # check that the game is running
        if self.playing == True:
            # every enemy object is in the self.enemies list, iterate through the list
            for i in self.enemies:
                # get the location of the object
                location_x = i.get_x_pos() 
                location_y = i.get_y_pos()
                # check the current tile of the object
                current_tile = self.game.get_tile(int(location_x/30), int(location_y/30)).get_coordinates()

                # check if the unit changed tile since last update
                if i.get_changed_tile() == False:
                    # if the unit is in the same tile as in the last update, find the next tile the unit is supposed to travel to
                    if 14 >= int(location_y/30) + 1 >= 0 and (self.game.get_tile(int(location_x/30), int(location_y/30) + 1).get_type() == "Road" or self.game.get_tile(int(location_x/30), int(location_y/30) + 1).get_type() == "End") and self.game.get_tile(int(location_x/30), int(location_y/30) + 1).get_coordinates().get_y() != i.get_last_tile().get_y():
                        i.set_pos(location_x, location_y + i.get_speed())
                        # check if the unit changed its tile after updating the position
                        if self.game.get_tile(int(location_x/30), int((location_y+i.get_speed())/30)).get_coordinates().get_y() != current_tile.get_y():
                            # if the unit changed tile set the direction it was going to and update the last tile
                            i.set_last_tile(current_tile)
                            i.tile_change()
                            i.reset_counter()
                            i.set_dir(1)
                        else:
                            i.set_tile_changed_false()
                            
                    elif 0 <= int(location_y/30) - 1 <= 14 and (self.game.get_tile(int(location_x/30), int(location_y/30) - 1).get_type() == "Road" or self.game.get_tile(int(location_x/30), int(location_y/30) - 1).get_type() == "End") and self.game.get_tile(int(location_x/30), int(location_y/30) - 1).get_coordinates().get_y() != i.get_last_tile().get_y():
                        i.set_pos(location_x, location_y - i.get_speed())
                        if self.game.get_tile(int(location_x/30), int((location_y - i.get_speed())/30)).get_coordinates().get_y() != current_tile.get_y():
                            i.set_last_tile(current_tile)
                            i.tile_change()
                            i.reset_counter()
                            i.set_dir(2)
                        else:
                            i.set_tile_changed_false()
                    
                    elif 0 <= int(location_x/30) + 1 <= 19 and (self.game.get_tile(int(location_x/30) + 1, int(location_y/30)).get_type() == "Road" or self.game.get_tile(int(location_x/30) + 1, int(location_y/30)).get_type() == "End") and self.game.get_tile(int(location_x/30) + 1, int(location_y/30)).get_coordinates().get_x() != i.get_last_tile().get_x():
                        i.set_pos(location_x + i.get_speed(), location_y)           
                        if self.game.get_tile(int((location_x + i.get_speed())/30), int(location_y/30)).get_coordinates().get_x() != current_tile.get_x():
                            i.set_last_tile(current_tile)
                            i.tile_change()
                            i.reset_counter()
                            i.set_dir(3)
                        else:
                            i.set_tile_changed_false()
                            
                    elif 19 >= int(location_x/30) - 1 >= 0 and (self.game.get_tile(int(location_x/30) - 1, int(location_y/30)).get_type() == "Road" or self.game.get_tile(int(location_x/30) - 1, int(location_y/30)).get_type() == "End") and self.game.get_tile(int(location_x/30) - 1, int(location_y/30)).get_coordinates().get_x() != i.get_last_tile().get_x():
                        i.set_pos(location_x - i.get_speed(), location_y)            
                        if self.game.get_tile(int((location_x - i.get_speed())/30), int(location_y/30)).get_coordinates().get_x() != current_tile.get_x():
                            i.set_last_tile(current_tile)
                            i.tile_change()
                            i.reset_counter()
                            i.set_dir(4)
                        else:
                            i.set_tile_changed_false()
                
                # when ever an unit changes its tile make it walk exactly tile_size/2 (checked with the counter in Enemy class) pixels to the direction it was going to in order to keep it in the middle of the path
                if i.get_changed_tile() == True:
                    direction = i.get_dir()
                    
                    if direction == "up":
                        i.set_pos(location_x, location_y + i.get_speed())
                        i.increase_counter()
                        
                    elif direction == "down":
                        i.set_pos(location_x, location_y - i.get_speed())
                        i.increase_counter()
                        
                    elif direction == "right":
                        i.set_pos(location_x + i.get_speed(), location_y)
                        i.increase_counter()
                        
                    elif direction == "left":
                        i.set_pos(location_x - i.get_speed(), location_y)
                        i.increase_counter()
                        
                    if i.get_counter() == self.tile_size/2:
                        i.set_tile_changed_false()
                
                # check if the unit has reached end tile, if it has add the Lose - screen to the scene
                
                if self.game.get_tile(int(location_x/30), int(location_y/30)).get_type() == "End":
                    self.lose_text1 = QGraphicsTextItem()
                    self.lose_text1.setFont(self.font)
                    self.lose_text1.setPos(215, 170)
                    self.lose_text1.setPlainText("YOU LOSE")
                    self.lose_text1.setDefaultTextColor(QColor(102, 0, 0))
                    self.lose_text2 = QGraphicsTextItem()
                    self.lose_text2.setFont(self.font)
                    self.lose_text2.setPos(90, 200)
                    self.lose_text2.setPlainText("PRESS R TO PLAY AGAIN")
                    self.lose_text2.setDefaultTextColor(QColor(102, 0, 0))
                    self.scene.addItem(self.lose_text1)
                    self.scene.addItem(self.lose_text2)
                    self.end = True
                    self.playing = False
    
    def update_towers(self):
        
        # updates the tower objects of the games. every tower is added to the self.towers list
        
        # check that the game is running
        if self.playing == True:
        
            # iterate through the list
            for i in self.towers:
                # check the tower position
                x = self.coordinatesToPixels(i.get_x_coord())
                y = self.coordinatesToPixels(i.get_y_coord())
                # iterate through enemies
                for n in self.enemies:
                    # calculate the delta x and delta y values for distance between the tower and the enemy
                    dx = abs(n.get_x_pos() - x)
                    dy = abs(n.get_y_pos() - y)
                    
                    # check if the tower doesnt have a target and if the enemy is in range of the tower
                    if i.get_target_status() == False and math.sqrt(dx*dx + dy*dy) <= i.get_range() and i.get_shoot_status() == True:
                        # if the tower has no target and enemy is in range, add it as the towers current target and shoot it
                        i.set_target(n.get_id())
                        i.shot()
                        # create a projectile object and set its position and target
                        projectile = Projectile(-3, -3, 6, 6)
                        projectile.set_pos(x, y)
                        projectile.set_target_x(n.get_x_pos())
                        projectile.set_target_y(n.get_y_pos())
                        # add the projectile to the scene and to the self.projectiles list
                        self.scene.addItem(projectile)
                        self.projectiles.append(projectile)
                        # hurt the enemy unit after shooting it
                        n.hurt(i.get_dmg())
                        # check if the enemy units hp is 0 or below, if it is the unit is dead and it is removed from the board and the player gets gold and score
                        if n.get_health() <= 0:
                            self.player_gold += n.get_bounty()
                            self.goldstatus.setPlainText("GOLD: " + str(self.player_gold))
                            self.score += n.get_score_value()
                            self.scorestatus.setPlainText("SCORE: " + str(self.score))
                            self.scene.removeItem(n)
                            self.enemies.remove(n)
                            i.delete_target()
                            
                    # if the tower already has a target and it is ready to shoot, fire at the current target
                    elif i.get_target_status() == True and n.get_id() == i.get_target_id() and i.get_shoot_status() == True:
                        # check if the target is still in range
                        if math.sqrt(dx*dx + dy*dy) <= i.get_range():
                            i.shot()
                            projectile = Projectile(-3, -3, 6, 6)
                            projectile.set_pos(x, y)
                            projectile.set_target_x(n.get_x_pos())
                            projectile.set_target_y(n.get_y_pos())
                            self.scene.addItem(projectile)
                            self.projectiles.append(projectile)
                            n.hurt(i.get_dmg())
                            # check if the enemy units hp is 0 or below, if it is the unit is dead and it is removed from the board and the player gets gold and score
                            if n.get_health() <= 0:
                                self.player_gold += n.get_bounty()
                                self.goldstatus.setPlainText("GOLD: " + str(self.player_gold))
                                self.score += n.get_score_value()
                                self.scorestatus.setPlainText("SCORE: " + str(self.score)) 
                                self.scene.removeItem(n)
                                self.enemies.remove(n)
                                i.delete_target()
                        # if the target is not in range anymore, delete the current target      
                        else:
                            i.delete_target()
                    # check if another tower killed the target
                    elif i.get_target_status() == True and i.get_shoot_status() == True:
                        i.delete_target()

    
    def update_projectiles(self):
        # updates the projectiles that are created whenever a tower shoots at target
        # check if the game is running
        if self.playing == True:
            for i in self.projectiles:
                # check the current position of the projectile
                position_x = i.get_x_pos()
                position_y = i.get_y_pos()
                # check the destination of the projectile
                destination_x = i.get_target_x()
                destination_y = i.get_target_y()
                # calculate the delta x and delta y values for updating the position
                dx = abs(destination_x - position_x)
                dy = abs(destination_y - position_y)
                # calculate the alpha angle from tangent so that the x and y values can be updated evenly
                alpha = math.atan2(dy, dx)
                
                # remove the projectile if it has no target or if it has reached the target destination
                if destination_x == None or destination_y == None or ( position_x == destination_x and position_y == destination_y ):
                    self.scene.removeItem(i)
                    self.projectiles.remove(i)
                
                # update the position of the projectile if it has not reached its target
                elif position_x != destination_x and position_y != destination_y:
                    x = math.cos(alpha)*i.get_speed()
                    y = math.sin(alpha)*i.get_speed()
                    
                    if position_x < destination_x and position_y < destination_y:
                    
                        if position_x + x > destination_x:
                            update_x = destination_x
                        else:
                            update_x = position_x + x
                            
                        if position_y + y > destination_y:
                            update_y = destination_y
                        else:
                            update_y = position_y + y
        
                        i.set_pos(update_x, update_y)
                        
                    elif position_x < destination_x and position_y > destination_y:
                    
                        if position_x + x > destination_x:
                            update_x = destination_x
                        else:
                            update_x = position_x + x
                            
                        if position_y - y < destination_y:
                            update_y = destination_y
                        else:
                            update_y = position_y - y
        
                        i.set_pos(update_x, update_y)
                        
                        
                    elif position_x > destination_x and position_y < destination_y:
                    
                        if position_x - x < destination_x:
                            update_x = destination_x
                        else:
                            update_x = position_x - x
                            
                        if position_y + y > destination_y:
                            update_y = destination_y
                        else:
                            update_y = position_y + y
        
                        i.set_pos(update_x, update_y)
                        
                    elif position_x > destination_x and position_y > destination_y:
                    
                        if position_x - x < destination_x:
                            update_x = destination_x
                        else:
                            update_x = position_x - x
                            
                        if position_y - y < destination_y:
                            update_y = destination_y
                        else:
                            update_y = position_y - y
        
                        i.set_pos(update_x, update_y)
                
                elif position_x == destination_x and position_y != destination_y:
                        
                        if position_y < destination_y:
                            if position_y + i.get_speed() > destination_y:
                                update_y = destination_y
                            else:
                                update_y = position_y + i.get_speed()

                        elif position_y > destination_y:
                            if position_y - i.get_speed() < destination_y:
                                update_y = destination_y
                            else:
                                update_y = position_y - i.get_speed()
            
                            i.set_pos(position_x, update_y)
                            
                elif position_y == destination_y and position_x != destination_x:
                        
                        if position_x < destination_x:
                            if position_x + i.get_speed() > destination_x:
                                update_x = destination_x
                            else:
                                update_x = position_x + i.get_speed()

                        elif position_x > destination_x:
                            if position_x - i.get_speed() < destination_x:
                                update_x = destination_x
                            else:
                                update_x = position_x - i.get_speed()
            
                            i.set_pos(update_x, position_y)
     
    def spawn_enemy(self):
        
        # method that is called by the self.enemytimer, spawns enemies every 1.5 seconds. checks how many enemies have been spawned with the self.enemy_counter value. spawns different enemies according to this value
        
        if self.playing == True:
            
            # spawns normal, basic enemies
            if self.enemy_counter != 5 and self.enemy_counter != 10:
                enemy = BasicEnemy()
                enemy.set_pos(self.coordinatesToPixels(self.spawnpoint.get_x()), self.coordinatesToPixels(self.spawnpoint.get_y()))
                enemy.set_last_tile(self.spawnpoint)
                self.enemies.append(enemy)
                self.scene.addItem(enemy)
                self.enemy_counter += 1
            
            # spawns an big enemy
            if self.enemy_counter == 5:
                enemy = BigEnemy()
                enemy.set_pos(self.coordinatesToPixels(self.spawnpoint.get_x()), self.coordinatesToPixels(self.spawnpoint.get_y()))
                enemy.set_last_tile(self.spawnpoint)
                self.enemies.append(enemy)
                self.scene.addItem(enemy)
                self.enemy_counter += 1
            
            # spawns an fast enemy, resets the counter
            if self.enemy_counter == 10:
                enemy = FastEnemy()
                enemy.set_pos(self.coordinatesToPixels(self.spawnpoint.get_x()), self.coordinatesToPixels(self.spawnpoint.get_y()))
                enemy.set_last_tile(self.spawnpoint)
                self.enemies.append(enemy)
                self.scene.addItem(enemy)
                self.enemy_counter = 0
        
     
    def paint(self, painter, option, widget):
        
        # paint a line that seperates the board from the UI, called once when the game is started
        
        if self.playing == True and self.painted == False:
            self.painted = True
            painter.setPen(QPen(Qt.black, 3))
            painter.drawLine(0,450,600,450)
            painter.setPen(QPen(Qt.black, 1))
            
        else:
            pass

    def coordinatesToPixels(self, i):
        # calculates and returns the middle point of a tile in pixels with the given coordinate i (int). has to be called seperately for x and y values
        val = i*self.tile_size + self.tile_size/2
        return val
        
    def initGame(self):
        # init the game when Start Game button is pressed
        self.clearMainMenu()
        self.addGridItems()
        self.drawUI()
        self.playing = True
        self.update()
    
    def addGridItems(self, mapfile = "roundmap.txt"):
            # creates the tile map of the game (20x15), if mapfile is not specified use testmap.txt
            # init x and y for tile identification
            x = 0
            y = 0
            # init a list of x tiles, this list is passed to self.game (GameWorld) once it's filled
            xtiles = []
            # bool values that are used in identifying multiple start/end positions
            start_set = False
            end_set = False
            
            try:
                # open the file
                with open(mapfile, 'r') as gamemap:
                    # iterate through every line and every character
                    for line in gamemap:
                        for char in line:
                            # identify the letter/number to set the correct tile type in place and do stuff accordingly
                            if char == '0':
                                square = QGraphicsRectItem(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                square.setBrush(QColor(211, 211, 211))
                                self.scene.addItem(square)
                                tile = Tile(x, y)
                                xtiles.append(tile)
                                x += 1
                                
                            elif char == '1':
                                square = QGraphicsRectItem(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                square.setBrush(QColor(153, 76, 0))
                                self.scene.addItem(square)
                                tile = Tile(x, y)
                                tile.set_type(1)
                                xtiles.append(tile)
                                x += 1

                            elif char == 'X':
                                square = QGraphicsRectItem(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                square.setBrush(QColor(100, 100, 100))
                                self.scene.addItem(square)
                                tile = Tile(x, y)
                                tile.set_type(2)
                                xtiles.append(tile)
                                x += 1

                            elif char == 'S':
                                if start_set == False:
                                    start_set = True
                                    square = QGraphicsRectItem(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                    square.setBrush(QColor(255, 255, 0))
                                    self.scene.addItem(square)
                                    tile = Tile(x, y)
                                    self.spawnpoint = Coordinates(x, y)
                                    tile.set_type(3)
                                    xtiles.append(tile)
                                    x += 1
                                else:
                                    raise CorruptedFileError("Corrupted map file (multiple start positions)")                                

                            elif char == 'E':
                                if end_set == False:
                                    end_set = True
                                    square = QGraphicsRectItem(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                                    square.setBrush(QColor(255, 0, 0))
                                    self.scene.addItem(square)
                                    tile = Tile(x, y)
                                    self.endpoint = Coordinates(x, y)
                                    tile.set_type(4)
                                    xtiles.append(tile)
                                    x += 1
                                else:
                                    raise CorruptedFileError("Corrupted map file (multiple end positions)")
                                
                            elif char == '\n':
                                pass
                                
                            else:
                                raise CorruptedFileError("Corrupted map file (unknown char)")
                        # x has to be exactly 20
                        if x != 20:
                            raise CorruptedFileError("Corrupted map file (invalid formating)")
                            
                        self.game.add_tiles(xtiles)
                        xtiles = []
                        x = 0
                        y += 1
                    # y has to be exactly 15 
                    if y != 15:
                        raise CorruptedFileError("Corrupted map file (invalid formating)")
                        
                    # close the file
                    gamemap.close
                    
            # if the file reading fails / file is not found:
            except OSError:
                raise  CorruptedFileError("Reading the map file failed")
       
    def drawUI(self):
        
        # draws the UI of the game using the Button class and QGraphicsTextItems
        
        self.buildbutton = Button(80, 80, 141, 141 , 141)
        self.buildbutton.setPos(70, 485)
        self.scene.addItem(self.buildbutton)

        self.buttoninfo1 = QGraphicsTextItem()
        self.buttoninfo1.setPos(92, 500)
        self.buttoninfo1.setPlainText("Tower")
        self.scene.addItem(self.buttoninfo1)
        
        self.buttoninfo2 = QGraphicsTextItem()
        self.buttoninfo2.setPos(80, 520)
        self.buttoninfo2.setPlainText("Cost: 100G")
        self.scene.addItem(self.buttoninfo2)
        
        self.buildmenu = QGraphicsTextItem()
        self.buildmenu.setPos(10, 460)
        self.buildmenu.setPlainText("BUILD:")
        self.scene.addItem(self.buildmenu)
        
        self.goldstatus = QGraphicsTextItem()
        self.goldstatus.setPos(240, 505)
        self.goldstatus.setPlainText("GOLD: " + str(self.player_gold))
        self.scene.addItem(self.goldstatus)
        
        self.scorestatus = QGraphicsTextItem()
        self.scorestatus.setPos(240, 520)
        self.scorestatus.setPlainText("SCORE: " + str(self.score))
        self.scene.addItem(self.scorestatus)
		
 
    def mousePressEvent(self, event):
        # handles mouse press events, checks the position of the click and does stuff accordingly
        x = event.pos().x()
        y = event.pos().y()
        # if the game is still in main menu check if either of the buttons are clicked
        if self.playing == False and self.end == False:
            if x > 150 and x < 450 and y > 200 and y < 250:
                self.initGame()
            elif x > 150 and x < 450 and y > 300 and y < 350:
                exit()
        # if the game is running
        if self.playing == True:
            # check if player is building something but does not click on a tile, clear the selection of the button (the Y pixel coordinates of the tiles are all < 450)
            if y > 450 and self.buildbutton.getStatus() == True:
                self.buildbutton.setFalse()
            # check if the player tries to build tower
            if y < 450 and self.buildbutton.getStatus() == True and self.game.get_tile(int(x/30), int(y/30)).get_type() == "Tower":
                # check if the player has enough gold
                if self.player_gold < 100:
                    self.update_status_msg("Not enough gold")
                    self.buildbutton.setFalse()
                # build the tower if player has enough gold
                elif self.game.get_tile(int(x/30), int(y/30)).set_tower() == True and self.player_gold >= 100:
                    # substitute the cost from player's gold
                    self.player_gold -= 100
                    # update the gold value shown on screen
                    self.goldstatus.setPlainText("GOLD: " + str(self.player_gold))
                    # add the tower to the self.towers list
                    self.towers.append(self.game.get_tile(int(x/30), int(y/30)).get_tower())
                    # create a status message
                    self.update_status_msg("Tower placed")
                    # change the color of the tile
                    square = QGraphicsRectItem(int(x/30)*self.tile_size, int(y/30)*self.tile_size, self.tile_size, self.tile_size)
                    square.setBrush(QColor(0, 204, 0))
                    self.scene.addItem(square)
                    # clear the selection of the build button
                    self.buildbutton.setFalse()
                # if all else fails, the tile the player tried constructing on already has a tower in it
                else:
                    # create a status message
                    self.update_status_msg("Tile already has a tower in it")
                    # clear sleection
                    self.buildbutton.setFalse()
            # check if the player tries to build a tower to an invalid tile (e.g. road)     
            if y < 450 and self.buildbutton.getStatus() == True and self.game.get_tile(int(x/30), int(y/30)).get_type() != "Tower":
                self.update_status_msg("Invalid tile")
                self.buildbutton.setFalse()

    def select(self, x, y):
        # used in debugging, takes two int arguments x and y which are used to get information about the tile that is in those coordinates
        print("x: " + str(self.game.get_tile(x,y).get_coordinates().get_x()) + " y: " + str(self.game.get_tile(x,y).get_coordinates().get_y()))

    def clearMainMenu(self):
        # clears the buttons and text items of the main menu
        self.scene.removeItem(self.startbutton)
        self.scene.removeItem(self.quitbutton)
        self.scene.removeItem(self.text1)
        self.scene.removeItem(self.text2)
        self.scene.removeItem(self.titletext)
        
    def update_status_msg(self, string):
        # called whenever a status message needs to be shown on the screen (e.g. if the player tries to construct a tower but does not have enough gold)
        self.status_message.setPlainText(string)
        # starts the timer which calls clear_status method after 4 seconds
        self.statustimer.start(4000)
    
    def clear_status(self):
        # clears the status message
        self.status_message.setPlainText("")
        

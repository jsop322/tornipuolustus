
class GameWorld():
    '''
    class that is used for saving the tile set of the map in a 2 dimensional list. can be used for e.g. getting the tile from a set of coordinates
    '''
    def __init__(self): 
        self.tiles = []
 
    def get_tile(self, x, y):
        # returns a tile from the given two int x and int y values (Tile)
        return self.tiles[y][x]
    
    def add_tiles(self, tilelist):
        # takes a list which represents an single row of tiles, add the list to the tiles list
        self.tiles.append(tilelist)
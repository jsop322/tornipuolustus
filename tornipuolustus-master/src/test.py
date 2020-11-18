import unittest
import sys
from io import StringIO
from tower_defence import TowerDefence
from corrupted_file_error import CorruptedFileError
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication

class Test(unittest.TestCase):
    # init one instance of QApplication
    app = QApplication(sys.argv)
    
    def test_unknown_character(self):
        # test if the map file has unknown characters that do not correspond to any tile type
        # create a dummy scene which is required in TowerDefence() class initialization
        self.scene = QGraphicsScene()
        # location of the broken test map
        test_data = "test/brokenmap_invalidchar.txt"
        
        check_this = None

        try:
            TowerDefence(self.scene).addGridItems(test_data)

        except CorruptedFileError as e:
            check_this = e
        
        self.assertEqual("Corrupted map file (unknown char)", str(check_this))
      
    def test_unknown_outofbounds_x(self):
        # test if the map file has too many characters in x axis
        self.scene = QGraphicsScene()

        test_data = "test/brokenmap_outofbounds_x.txt"
        
        check_this = None

        try:
            TowerDefence(self.scene).addGridItems(test_data)

        except CorruptedFileError as e:
            check_this = e
        
        self.assertEqual("Corrupted map file (invalid formating)", str(check_this))

    def test_unknown_outofbounds_y(self):
        # test if the map file has too many characters in y axis
        self.scene = QGraphicsScene()
        
        test_data = "test/brokenmap_outofbounds_y.txt"
        
        check_this = None
     
        try:
            TowerDefence(self.scene).addGridItems(test_data)

        except CorruptedFileError as e:
            check_this = e
        
        self.assertEqual("Corrupted map file (invalid formating)", str(check_this))


    def test_invalid_formating(self):
        # test if the map file is missing characters in rows/columns
        self.scene = QGraphicsScene()

        test_data = "test/brokenmap_invalid_formating.txt"
        
        check_this = None

        try:
            TowerDefence(self.scene).addGridItems(test_data)

        except CorruptedFileError as e:
            check_this = e
        
        self.assertEqual("Corrupted map file (invalid formating)", str(check_this))

    def test_multiple_starts(self):
        # test if the map file has multiple start positions
        self.scene = QGraphicsScene()

        test_data = "test/brokenmap_multiple_starts.txt"

        check_this = None

        try:
            TowerDefence(self.scene).addGridItems(test_data)

        except CorruptedFileError as e:
            check_this = e
        
        self.assertEqual("Corrupted map file (multiple start positions)", str(check_this))

    def test_multiple_ends(self):
        # test if the map file has multiple end positions
        self.scene = QGraphicsScene()

        test_data = "test/brokenmap_multiple_ends.txt"
        
        check_this = None
     
        try:
            TowerDefence(self.scene).addGridItems(test_data)

        except CorruptedFileError as e:
            check_this = e
        
        self.assertEqual("Corrupted map file (multiple end positions)", str(check_this))
        
    def test_missing_file(self):
        # test if the map file does not exist
        self.scene = QGraphicsScene()

        test_data = "test/this_file_does_not_exist.txt"
        
        check_this = None
     
        try:
            TowerDefence(self.scene).addGridItems(test_data)

        except CorruptedFileError as e:
            check_this = e
        
        self.assertEqual("Reading the map file failed", str(check_this))

if __name__ == '__main__':
    unittest.main()
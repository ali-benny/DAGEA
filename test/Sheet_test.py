#from Sheet import Sheet as s
import src.pythonModules.fantacitorio.Sheet as s

# Librerie di testing
import unittest

sheetPath = "../src/pythonModules/fantacitorio/punti.xlsx"
numberOfTurns = 9

class TestAPIv2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        s.Sheet.__init__(path=sheetPath, numberOfTurns=numberOfTurns)

    def test___init__(self):
        with self.assertRaises(Exception) as exc:
            s.Sheet.__init__("errorTest.html", numberOfTurns=numberOfTurns)
            self.assertEquals(str(exc.exception), "Fantacitorio - Sheet.py - Incorrect input - __init__: Make sure the 'path' parameter ends with '.xlsx'")

        with self.assertRaises(Exception) as exc:
            s.Sheet.__init__(sheetPath, numberOfTurns=-1)
            self.assertEquals(str(exc.exception), "Fantacitorio - Sheet.py - Incorrect input - __init__: numberOfTurns can not be a negative number")

        self.setUpClass()
        self.assertEqual(s.Sheet.sheet_path, sheetPath)
        self.assertEqual(s.Sheet.numberOfTurns, numberOfTurns + 1)

        columnsLimits = {}
        turnsIndexes = range(1, s.Sheet.numberOfTurns)
        for i, s.Sheet.columnLimit in zip(turnsIndexes, s.Sheet.sheet_columnsLimits):
            columnsLimits.update({"turn" + str(i): s.Sheet.columnLimit})
        self.assertEqual(s.Sheet.columnsLimits, columnsLimits)

    def test_getTurnFromSheet(self):
        self.setUpClass()
        temp = s.Sheet.getTurnFromSheet(turn="turn1", tableFormat=True)
        self.assertEqual(s.Sheet.getTurnFromSheet(turn="turn1", tableFormat=True), temp)
        temp = s.Sheet.getTurnFromSheet(turn="turn1", tableFormat=False)
        self.assertEqual(s.Sheet.getTurnFromSheet(turn="turn1", tableFormat=False), temp)
        
    def test_getTurnsFromSheet(self):
        self.setUpClass()
        temp = s.Sheet.getTurnsFromSheet(tableFormat=False)
        self.assertEqual(s.Sheet.getTurnsFromSheet(tableFormat=False), temp)
        temp = s.Sheet.getTurnsFromSheet(tableFormat=True)
        self.assertEqual(s.Sheet.getTurnsFromSheet(tableFormat=True), temp)

    def test_getPlayedTurns(self):
        self.setUpClass()
        self.assertEqual(s.Sheet.getPlayedTurns(), list(s.Sheet.columnsLimits.keys()))

if __name__ == "__main__":
    unittest.main()

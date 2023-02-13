#from Fantacitorio import Fantacitorio as f
import src.pythonModules.fantacitorio.Fantacitorio as f

# Librerie di testing
import unittest

sheetPath = "../src/pythonModules/fantacitorio/punti.xlsx"
numberOfTurns = 9

class TestAPIv2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        f.Fantacitorio.__init__(path=sheetPath, numberOfTurns=numberOfTurns)

    def test___init__(self):
        self.setUpClass()
        turns = f.Fantacitorio.turns
        turnsInTableFormat = f.Fantacitorio.turnsInTableFormat
        names = f.Fantacitorio.names
        completeReport = f.Fantacitorio.completeReport
        simpleReport = f.Fantacitorio.simpleReport
        self.assertEqual(turns, f.Fantacitorio.getTurnsFromSheet(tableFormat=False))
        self.assertEqual(turnsInTableFormat, f.Fantacitorio.getTurnsFromSheet(tableFormat=True))
        self.assertEqual(names, f.Fantacitorio.getTurnsNames())
        self.assertEqual(completeReport, f.Fantacitorio.getCompleteReport())
        self.assertEqual(simpleReport, f.Fantacitorio.getSimpleReport())

if __name__ == "__main__":
    unittest.main()

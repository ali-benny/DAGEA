#from FantacitorioAnalysis import FantacitorioAnalysis as fa
import src.pythonModules.fantacitorio.FantacitorioAnalysis as fa

# Librerie di testing
import unittest

import os

sheetPath = "../src/pythonModules/fantacitorio/punti.xlsx"
numberOfTurns = 9

class TestAPIv2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fa.FantacitorioAnalysis.__init__(path=sheetPath, numberOfTurns=numberOfTurns)

    def test___init__(self):
        self.setUpClass()
        standings = fa.FantacitorioAnalysis.getStandings()
        dataFrame = fa.FantacitorioAnalysis.getDataFrame()
        self.assertEqual(fa.FantacitorioAnalysis.getStandings(), standings)
        '''
        fa.FantacitorioAnalysis.graph_politicians()
        fa.FantacitorioAnalysis.graph_turns()
        '''
        fa.FantacitorioAnalysis.getBestClimber()
        fa.FantacitorioAnalysis.getBWSingleScore(getBest=True)
        fa.FantacitorioAnalysis.getBWSingleScore(getBest=False)
        fa.FantacitorioAnalysis.getBWPlayer(getBest=True)
        fa.FantacitorioAnalysis.getBWPlayer(getBest=False)
        fa.FantacitorioAnalysis.getBWAverage(getBest=True)
        fa.FantacitorioAnalysis.getBWAverage(getBest=False)
        fa.FantacitorioAnalysis.getBWTurn(getBest=True)
        fa.FantacitorioAnalysis.getBWTurn(getBest=False)
        fa.FantacitorioAnalysis.getStats()

if __name__ == "__main__":
    unittest.main()

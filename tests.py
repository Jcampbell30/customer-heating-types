# the test suites are kept here
# NOTE: reference here. https://docs.python.org/3/library/unittest.html#module-unittest
import unittest
import pandas as pd
from InferenceLogic import *
from SpikeDetector import *
from Database import Database as db
from PlotAnalysis import *

class TestInferenceLogic(unittest.TestCase):
    
    def test_inferDynamic(self):
        self.assertEqual(inferDynamic(13, 8), {"Electric confidence:": 61.54, "Non-Electric confidence:": 38.46})
        self.assertIsInstance(inferDynamic(13, 8), dict)

class TestSpikeDetector(unittest.TestCase):

    def setUp(self):
        self.ds = [[20210101, 1.0], [202100102, 2.0]]

    def test_getSpikes(self):
        self.assertIsInstance(getSpikes(self.ds, 100), list)

class TestDatabase(unittest.TestCase):
    #NOTE: currently tests actual connections to db. It should test connection to a mock db to
        # ensure that the conenection logic works. TODO: fix in integration test

    def setUp(self):
        d = {'Date': [1, 2], 'col2': [3, 4]}
        self.df = pd.DataFrame(data=d)

    def test_retrievePowerFromDB(self):
        self.assertIsInstance(db.retrievePowerFromDB(self, 139920), pd.DataFrame)
    
    def test_retrieveTempFromDB(self):
        self.assertIsInstance(db.retrieveTempFromDB(self, self.df ), list)

class TestPlotAnalysis(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame

    #TODO: test_dailyAverage()

    #TODO: test_buildVisual()

if __name__ == '__main__':
    unittest.main(verbosity=2) #enables a higher level of verbosity to show which tests are running
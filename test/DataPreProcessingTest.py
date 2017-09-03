import unittest

from datapreprocessing import Main


class DataPreProcessingTest(unittest.TestCase):

    # set up app
    def setUp(self):
        self.app = Main()

    # dismantle app
    def tearDown(self):
        self.app.dispose()
        self.app = None


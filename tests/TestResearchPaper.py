import unittest
import csv
from collections.abc import Iterable

class TestResearchPaper(unittest.TestCase):

    def test_readCSV(self):
        filePath = r"data/rawData/SMdata.csv"
        with open(filePath, newline=None, encoding="utf-8") as csvFile:
            paperReader = csv.reader(csvFile)
            self.assertIs(paperReader, Iterable)
import unittest
import csv
import os

from src.Results import Results


class TestResults(unittest.TestCase):
    def setUp(self) -> None:
        self.results = Results("1", "1989", "Skilled financial planning: the cost of translating ideas into action",
                               "This research paper utilizes interviews and questionnaires as a data source and "
                               "think-aloud sessions as the data gathering methodology.")

    def test_appendToCSV(self):
        testResultsPath = r"testData/testResults.csv"
        self.results.appendToCSV(testResultsPath)
        self.assertTrue(os.path.isfile(testResultsPath))

    def test_appendToCSVWrittenText(self):
        expected = ['1', '1989', 'Skilled financial planning: the cost of translating ideas into action',
                    "This research paper utilizes interviews and questionnaires as a data source and think-aloud "
                    "sessions as the data gathering methodology."]
        testResultsPath = r"testData/testResults.csv"
        with open(testResultsPath, newline='', encoding="utf-8-sig") as csvfile:
            resultReader = csv.reader(csvfile, delimiter=',')
            actual = next(resultReader)
        self.assertEqual(expected, actual)

    def test_extractMethodologyClassification(self):
        actual = self.results._extractMethodologyClassification()
        expected = "interviews and questionnaires"
        self.assertEqual(expected, actual)

    def tearDown(self) -> None:
        del self.results

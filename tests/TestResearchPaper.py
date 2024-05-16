import csv
import unittest
from src.ResearchPaper import ResearchPaper
import os


class TestResearchPaper(unittest.TestCase):

    def setUp(self) -> None:
        self.researchPaper = ResearchPaper('0', '2002', 'Test Title', '@This@Is-ATest_Text[]*    Body.')

    def test_removeNonAlphaNumericsExceptDashesPeriods(self):
        expected = 'ThisIs-ATestText    Body.'
        self.researchPaper.removeNonAlphaNumericsExceptDashesPeriods()
        self.assertEqual(expected, self.researchPaper._text)

    def test_replaceDashesAndManySpacesWithSpace(self):
        expected = '@This@Is ATest_Text[]* Body.'
        self.researchPaper.replaceDashesAndManySpacesWithSpace()
        self.assertEqual(expected, self.researchPaper._text)

    def test_appendToCorpusCSV(self):
        preprocessedDataPath = r"testData/testPreprocessedChiData.csv"
        self.researchPaper.appendToCorpusCSV(preprocessedDataPath)
        self.assertTrue(os.path.isfile(preprocessedDataPath))

    def test_appendToCorpusCSVWrittenText(self):
        expected = ['0', '2002', 'Test Title', '@This@Is-ATest_Text[]*    Body.']
        preprocessedDataPath = r"testData/testPreprocessedChiData.csv"
        with open(preprocessedDataPath, newline='', encoding="utf-8-sig") as csvfile:
            paperReader = csv.reader(csvfile, delimiter=',')
            paper = next(paperReader)
        self.assertEqual(expected, paper)

    def tearDown(self) -> None:
        del self.researchPaper




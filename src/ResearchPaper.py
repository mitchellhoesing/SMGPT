import re


class ResearchPaper:
    def __init__(self, uid, year, title, text):
        self._uid = uid
        self._year = year
        self._title = title
        self._text = text

    def removeNonAlphaNumericsExceptDashesPeriods(self):
        # Remove non-alphanumeric characters except spaces and dashes.
        self._text = re.sub(r'[^A-Za-z0-9\s\.-]+', "", self._text)

    def replaceDashesAndManySpacesWithSpace(self):
        # Substitute a space where dashes and sequential spaces, greater than or equal to two, exist.
        self._text = re.sub(r'(-|\s{2,})', " ", self._text)

    def appendToCorpusCSV(self, preprocessedDataPath):
        with open(preprocessedDataPath, 'a', encoding='utf-8-sig') as fd:
            output = self._uid + "," + self._year + "," + self._title + "," + self._text + "\n"
            fd.write(output)





class Results:
    def __init__(self, uid, year, title, response):
        self._uid = uid
        self._year = year
        self._title = title
        self._response = response
        self._methodologyTaxonomy = ["brainstorming and focus groups", "interviews and questionnaires",
                                     "conceptual modeling", "work diaries", "think-aloud sessions",
                                     "shadowing and observation", "participant observation", "instrumenting systems",
                                     "fly on the wall", "analysis of work databases", "analysis of tool use logs",
                                     "documentation analysis", "static and dynamic analysis"]
        self.classification = self._extractMethodologyClassification()

    def appendToCSV(self, resultPath):
        with open(resultPath, 'a', encoding='utf-8-sig') as fd:
            output = self._uid + "," + self._year + "," + self._title + "," + self.classification + "\n"
            fd.write(output)

    def _extractMethodologyClassification(self):
        self._response = self._response.lower()
        for classification in self._methodologyTaxonomy:
            if classification in self._response:
                return classification

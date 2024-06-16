import numpy as np
import json
import re

class Results:
    def __init__(self, uid, year, title, response, taxonomy, userBasePrompt, serializedResponse):
        self._uid = uid
        self._year = year
        self._title = title
        self._response = response
        self._serializedResponse = serializedResponse
        self._taxonomy = taxonomy
        self.classifications = self._extractMethodologyClassification()
        self.logprobs = self._extractTopLogProbs()
        self._userBasePrompt = userBasePrompt

    def __repr__(self):
        result = f"\n{self._uid}, {self._year}, {self._title}, {self.classifications}\n"
        result += str(self._response.choices[0].message.content) + "\n\n"
        for logprob in self._response.choices[0].logprobs.content:
            for top_logprob in logprob.top_logprobs:
                result += f"Token: {str(top_logprob.token)} "
                result += f"logprob: {str(top_logprob.logprob)} "
                result += f"linear prob: {str(np.round(np.exp(top_logprob.logprob) * 100, 2))}\n"
            result += "\n"
        return result

    def appendToCSV(self, resultPath):
        with open(resultPath, 'a', encoding='utf-8-sig') as fd:
            output = f"{self._uid},{self._year},{self._title},{self.classifications},{self.logprobs}," \
                     f"\"{self._userBasePrompt}\"\n"
            fd.write(output)

    def _extractTopLogProbs(self):
        logprobs = ""
        for logprob in self._response.choices[0].logprobs.content:
            for top_logprob in logprob.top_logprobs:
                logprobs += f"Token: {str(top_logprob.token)}, logprob: {str(top_logprob.logprob)}, "\
                                f"linearprob: {str(np.round(np.exp(top_logprob.logprob) * 100, 2))} "

        logprobs = self._replacePredictedNewlines(logprobs)
        logprobs = self._replacePredictedQuotes(logprobs)
        return f"\"{logprobs}\""

    @staticmethod
    def _replacePredictedNewlines(inputString):
        outputString = inputString.replace('\n', '\\n')
        return outputString

    @staticmethod
    def _replacePredictedQuotes(inputString):
        outputString = inputString.replace('"', '')
        return outputString

    def appendToJSON(self, jsonPath):
        with open(jsonPath, "w+", encoding='utf-8-sig') as json_file:
            if not json_file:
                jsonContents = json.load(json_file)
            else:
                jsonContents = []
            jsonContents.append(self._serializedResponse)
            json.dump(self._serializedResponse, json_file)

    def _extractMethodologyClassification(self):
        classifications = ""
        self.responseText = self._response.choices[0].message.content
        self.responseText = self.responseText.lower()
        for classification in self._taxonomy:
            if classification in self.responseText:
                classifications += f"{classification},"
        if not classifications: # if list is empty
            return "\"DNE: " + self.responseText + "\""

        return f"\"{classifications}\""

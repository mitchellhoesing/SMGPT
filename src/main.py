import csv
from openai import OpenAI
import time
import os
from ResearchPaper import ResearchPaper
from src.Results import Results


def main():
    startTime = time.time()
    rawData = r"data/rawData/chiData.csv"
    preprocessedData = r"data/preprocessedData/preprocessedChiData.csv"
    resultsPath = r"results/results.csv"

    # # Program Control TODO: Implement command line arguments.
    preprocess = False
    APICalls = True

    if preprocess:
        if os.path.exists(preprocessedData):
            os.remove(preprocessedData)
        print("Preprocessing data...")
        with open(rawData, newline='', encoding="utf-8-sig") as rawText:
            paperReader = csv.reader(rawText)
            for row in paperReader:
                researchPaper = ResearchPaper(uid=row[0], year=row[1], title=row[2], text=row[3])
                researchPaper.removeNonAlphaNumericsExceptDashesPeriods()
                researchPaper.replaceDashesAndManySpacesWithSpace()
                researchPaper.appendToCorpusCSV(preprocessedData)
        print("--- Preprocess run time: %s seconds ---" % (time.time() - startTime))
    else:
        print('Skipping preprocessing...')

    if APICalls:
        client = OpenAI()
        taxonomyPrompt = "Data methodology taxonomy: Brainstorming and focus groups, Interviews and questionnaires," \
                         "Conceptual modeling, Work diaries, Think-aloud sessions, shadowing and observation, " \
                         "Participant observation, Instrumenting systems, Fly on the wall, Analysis of work databases," \
                         "Analysis of tool use logs, Documentation analysis, Static and dynamic analysis."

        with open(preprocessedData, newline='', encoding="utf-8-sig") as rawText:
            paperReader = csv.reader(rawText)
            next(paperReader)
            for row in paperReader:
                uid = row[0]
                year = row[1]
                title = row[2]
                text = row[3]
                '''
                Roles: 
                System: The system message helps set the behavior of the assistant. For example, you can modify the personality
                of the assistant or provide specific instructions about how it should behave throughout the conversation.
                However note that the system message is optional and the model’s behavior without a system message is likely to
                be similar to using a generic message such as "You are a helpful assistant.

                User: The user messages provide requests or comments for the assistant to respond to.

                Assistant: Assistant messages store previous assistant responses, but can also be written by you to give 
                examples of desired behavior.
                
                Parameter:
                top_p: An alternative to sampling with temperature, called nucleus sampling, where the
                  model considers the results of the tokens with top_p probability mass. So 0.1
                  means only the tokens comprising the top 10% probability mass are considered.
                '''
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=[
                        # {"role": "system", "content": "You are to classify the provided research paper's data source "
                        #                               "and data gathering methodology into the provided taxonomy. "
                        #                               "Respond with only your classifications.\n" + taxonomyPrompt +
                        #                               "Research paper:\n" + text},
                        {"role": "user", "content": "Research paper:\n" + text + "\n" + taxonomyPrompt +
                                                    "\nClassification: Data source and data gathering methodology - "
                                                    "You are to classify the provided research paper's data source and "
                                                    "data gathering methodology into one category in the provided "
                                                    "taxonomy, in the format of the following sentence, filling in the "
                                                    "[MASK] tokens."
                                                    "This research paper utilizes [MASK] as a data source and [MASK] "
                                                    "is the data gathering methodology."}
                         #} Respond with only your classification.

                    ],
                    # Temperature = 0 to favor highest probability token in generation
                    temperature=0,
                    max_tokens=256,
                    # top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    logprobs=True,
                    top_logprobs=5
                )
                classification = response.choices[0].message.content
                results = Results(uid, year, title, classification)
                results.appendToCSV(resultsPath)


                print(f"{uid}, {year}, {title}, {classification}")
                print(response.choices[0].logprobs.content)
                print(response)
                break

    else:
        print("Skipping API Calls")


if __name__ == '__main__':
    main()

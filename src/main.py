import csv
from openai import OpenAI
from openai.types import CreateEmbeddingResponse
import time
import os
from ResearchPaper import ResearchPaper
from src.Results import Results


def main():
    startTime = time.time()
    rawData = r"data/rawData/chiData.csv"
    preprocessedData = r"data/preprocessedData/preprocessedChiData.csv"
    resultsPath = r"results/results.csv"
    resultsJson = r"results/serializedResults.json"

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
        print("Making API calls...")
        client = OpenAI()
        methodologyTaxonomy = "brainstorming and focus groups: In brainstorming, several people get together and " \
                              "focus on a particular issue. The idea is to ensure that discussion is not limited to " \
                              "“good” ideas or ideas that make immediate sense, but rather to uncover as many ideas " \
                              "as possible. Focus Groups are similar to brainstorming. However, focus groups occur " \
                              "when groups of people are brought together to focus on a particular issue (not just " \
                              "generate ideas). They also involve moderators to focus the group discussion and make " \
                              "sure that everyone has an opportunity to participate. " \
                              "interviews: Interviews involve at least one researcher talking to at least one " \
                              "respondent. Interviews can be conducted in two ways. In a structured interview, " \
                              "a fixed list of carefully worded questions forms the basis of the interview. Usually, " \
                              "the questions are asked exactly as written, and no deviations occur. The data from " \
                              "structured interviews is usually analysed using statistical analyses. In a " \
                              "semi-structured interview, the interview generally follows more of a conversational " \
                              "flow. New questions may be devised as new information is learned." \
                              "questionnaires: Questionnaires are sets of questions administered in a written or " \
                              "digital format." \
                              "conceptual modeling: During conceptual modeling, participants create a model of some " \
                              "aspect of their work – the intent is to bring to light their mental models. In its " \
                              "simplest form, participants draw a diagram of some aspect of their work. For instance, " \
                              "software engineers may be asked to draw a data flow diagram, a control flow diagram or " \
                              "a package diagram showing the important architectural clusters of their system. As an " \
                              "orthogonal usage, software engineers may be asked to draw a physical map of their " \
                              "environment, pointing out who they talk to and how often." \
                              "work diaries: Work diaries require respondents to record various events that occur " \
                              "during the day. It may involve filling out a form at the end of the day, " \
                              "recording specific activities as they occur, or noting whatever the current task is at " \
                              "a pre-selected time. These diaries may be kept on paper or in a computer." \
                              "think-aloud sessions: In think-aloud protocol analysis, researchers ask participants " \
                              "to think out loud while performing a task. The task can occur naturally at work or be " \
                              "predetermined by the researcher." \
                              "shadowing: In shadowing, the experimenter follows the participant around and records " \
                              "their activities. Shadowing can occur for an unlimited time period, as long as there " \
                              "is a willing participant." \
                              "participant-observer: Usually done as part of an ethnography, in the " \
                              "participant-observer technique, the researcher essentially becomes part of the team " \
                              "and participates in key activities." \
                              "instrumenting systems: This technique requires “instrumentation” to be built into the " \
                              "software tools used by the software engineer. This instrumentation is used to record " \
                              "information automatically about the usage of the tools. Instrumentation can be used to " \
                              "monitor how frequently a tool or feature is used, patterns of access to files and " \
                              "directories, and even the timing underlying different activities. This technique is " \
                              "also called system monitoring. In some cases, instrumentation merely records the " \
                              "commands issued by users. More advanced forms of instrumentation record both the input " \
                              "and output in great detail so that the researcher can effectively play back the " \
                              "session." \
                              "fly on the wall: “Fly on the Wall” is a hybrid technique. It allows the researcher to " \
                              "be an observer of an activity without being present. Participants are asked to video " \
                              "or audiotape themselves when they are engaged in some predefined activity." \
                              "document corpus analysis: This is the analysis of data corpora derived from textual " \
                              "data such as electronic databases of performed work, tool logs, commit histories, " \
                              "code, repositories, documentation, and website scraping." \
                              "social media analysis: This is the analysis of data deriving from social media " \
                              "websites. This could be from scraping social media websites or using their APIs." \
                              "image, audio, and video library analysis: This is the analysis of a collection of " \
                              "image, audio, and/or video files not created by the researchers in the research " \
                              "paper." \
                              "lab experiment: These are conducted under controlled conditions, in which the " \
                              "researcher deliberately changes something (independent variable) to see the effect of " \
                              "this on something else (dependent variable)" \
                              "no experiment: These are research papers that did not perform a experiment." \
            # Added: social media analysis, website analysis, online surveys and polls for amazon mechanical turk/crowd workers.
        # Split: interviews and questionnaires
        # "work database analysis, "
        # "tool use log analysis," \ Combined work database analysis, tool use log analysis and documentation analysis.
        # "static and dynamic analysis" Not going to see in CHI.

        # sourceTaxonomy = "mouse and keyboard interaction data, " \
        #                  "touch interaction data, " \
        #                  "voice interaction data, " \
        #                  "gaze tracking data, " \
        #                  "gesture data, " \
        #                  "other sensor data, " \
        #                  "musical data, " \
        #                  "video data, " \
        #                  "video games data, " \
        #                  "augmented or virtual reality data, " \
        #                  "facebook social media data, " \
        #                  "twitter social media data, " \
        #                  "youtube social media data, " \
        #                  "reddit social media data, " \
        #                  "other social media data, " \
        #                  "web scraped data, " \
        #                  "internet-of-things data, " \
        #                  "design artifact data, " \
        #                  "revision history data, " \
        #                  "physiological data, " \
        #                  "emotional response data, " \
        #                  "ethnographic data, " \
        #                  "system log data, " \
        #                  "team chat log data, " \
        #                  "not clear"
        taxonomy = ['brainstorming and focus groups', 'interviews', 'questionnaires', 'conceptual modeling',
                    'word diaries', 'think-aloud sessions', 'shadowing', 'participant-observer', 'instrumenting systems'
                    , 'fly on the wall', 'document corpus analysis', 'social media analysis',
                    'image audio and video library analysis', 'lab experiment', 'no experiment']
        taxonomy = list(map(str.strip, taxonomy))

        taxonomyPrompt = f"Data gathering methodology taxonomy and taxa definitions: {methodologyTaxonomy}"
        userBasePrompt = "What are the data gathering methodologies of this research paper according to our taxonomy? " \
                         "Answer in the format of the following " \
                         "sentence. The set of this research paper's data gathering " \
                         "methodologies contains [MASK]."
        # Classify the data gathering method(s) into any applicable classes in the data methodology gathering taxonomy.

        # "You are to perform a single or multiclass classification of the provided research " \
        # "paper's data gathering methodology.

        # filling in the [MASK] token with a set of any length containing methodologies that match best.
        with open(preprocessedData, newline='', encoding="utf-8-sig") as rawText:
            paperReader = csv.reader(rawText)
            next(paperReader)
            for row in paperReader:
                # if paperReader.line_num != 6455 + 1: # Dodge starcraft paper

                # if paperReader.line_num != 6250 + 1: # binns paper. group truth: interviews, lab-based studies, online experiments, and think-aloud sessions.

                # if paperReader.line_num != 882 + 1:

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

                userFinalPrompt = f"Your task is to classify the data gathering methodology of the following research " \
                                  f"paper into our provided data gathering " \
                                  f"methodology taxonomy. Classification: Data gathering methodology - " \
                                  f"Research paper:\n{text}\n{taxonomyPrompt}\n{userBasePrompt} "

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=[
                        {"role": "system", "content": "You are a professional CHI research scientist."},
                        {"role": "user", "content": userFinalPrompt}
                        # If the data source is not clear then "
                        #                                      "answer "
                        # \"The data source is not listed in the above data source "
                        #  "taxonomy.\"
                        # "utilizes [MASK] as a data source and [MASK] is the data "
                        # "gathering methodology."}
                        # The data source is not listed in the above data source taxonomy.
                        # } Respond with only your classification.

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
                serializedResponse = response.model_dump_json()
                results = Results(uid, year, title, response, taxonomy, userBasePrompt, serializedResponse)
                results.appendToCSV(resultsPath)
                results.appendToJSON(resultsJson)

                # print(results)

    else:
        print("Skipping API Calls")


if __name__ == '__main__':
    main()

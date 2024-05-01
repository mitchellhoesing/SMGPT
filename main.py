from openai import OpenAI


def main():

    client = OpenAI()
    # Program Control TODO: Implement command line arguments.
    preprocess = False
    if preprocess:
        pass
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming "
                                          "concepts with creative flair."},
            {"role": "user", "content": "Compose a one word poem that explains the concept of recursion in programming."}

        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response.choices[0].message.content)
    #print(response)


if __name__ == '__main__':
    main()


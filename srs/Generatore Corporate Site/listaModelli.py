import openai
openai.api_key = "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"

def ChatGPT_test(conversation):
    # create a chat completion
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
    api_usage=response['usage']
    print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # print the chat completion
    print(response.choices[0].message.content)

conversation = []
conversation.append({'role':'system','content':'quale modello di openAi può essermi più utile per modificare codice?'})
ChatGPT_test(conversation)
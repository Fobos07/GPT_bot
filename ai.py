import openai
import json

from cfg import ai_key
from db import response_data, add_new_request, minus_tokens, check_tokens


openai.api_key = ai_key

class NewUser:
    def __init__(self, id) -> None:
        self.id = id
        with open('data.json', 'r') as fp:
            try:
                data = json.load(fp)
            except:
                data = {str(self.id): []}
        if str(self.id) not in list(data['users'].keys()):
            data['users'].update({self.id: []})
            with open('data.json', 'w') as fp:
                fp.write(json.dumps(data, indent=4))
            

class ToChatGPT():
    def __init__(self, id, text) -> None:
        self.id = id
        self.text = text


    def chat_with_gpt(self):
        with open('data.json', 'r') as fp:
            try:
                data = json.load(fp)
            except:
                data = {str(self.id): []}
        
        prompt = f"{'; '.join(data['users'][str(self.id)])}; {self.text}"
        if check_tokens(self.id) <= 0:
            return 'Вы потратили '
        
        if len(prompt) >= 900:
            prompt = prompt[500:]

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        with open('data.json', 'w') as fp:
            data['users'][str(self.id)].append(self.text)
            fp.write(json.dumps(data, indent=4))
        if response['choices'][0]['text'][:1] == ';':
            answer = response['choices'][0]['text'][1:]
        else: answer = response['choices'][0]['text']
        
        minus_tokens(id=self.id, length=len(prompt))
        return(answer)

class ClearData():
    def clear_history(self, id):
        self.id = id
        with open('data.json', 'r') as fp:
            try:
                data = json.load(fp)
                print(data)
            except:
                data = {str(self.id): []}
        
        with open('data.json', 'w') as fp:
            data['users'][str(self.id)].clear()
            fp.write(json.dumps(data, indent=4))
# ToChatGPT(334019728, 'Расскажи подробнее').clear_history()
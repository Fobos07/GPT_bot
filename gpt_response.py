import json
import openai
from openai.error import InvalidRequestError

from cfg import ai_key, roles
from db import check_user_role, minus_tokens

openai.api_key = ai_key

class GptResponse():
    def __init__(self, id: int, message: str) -> None:
        self.id = str(id)
        self.message = str(message)
        with open('data.json', 'r') as fp:
            self.data = json.load(fp)

    def main(self) -> str:
        try:
            if len(self.data[self.id]) == 0:
                self.data[self.id].append(roles[check_user_role(self.id)])
            else:
                self.data[self.id][0] = (roles[check_user_role(self.id)])
            self.data[self.id].append({"role": "user", "content": self.message})
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.data[self.id]
                )
            self.data[self.id].append({'role': 'assistant', 'content': completion.choices[0].message.content})
            with open('data.json', 'w') as fp:
                fp.write(json.dumps(self.data, indent=4, ensure_ascii=False))
            minus_tokens(completion.usage.completion_tokens, self.id)
            return completion.choices[0].message.content
        except InvalidRequestError:
            if len(self.data[self.id]) >= 3:
                self.data[self.id].pop(1)
                self.main()
            else: return 'Слишком длинный запрос, сократи текст!'
        else: 
            return 'Произошла неизвестная ошибка, задай вопрос еще раз :('
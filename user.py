import json
from db import add_user, check_tokens, add_user_role, minus_tokens
from cfg import buy_tokens, roles
from datetime import datetime


class NewUser:
    def __init__(self, id: int, name: str, username: str) -> None:
        self.id = id
        self.name = name
        self.username = username
        self.role = 'Роль не установлена'
        self.time = str(datetime.today())
        add_user([self.id, self.name, self.username, 'Нет подписки:(', 3000, self.role, self.time])
        with open('data.json', 'r') as fp:
            try:
                data = json.load(fp)
            except:
                data = {str(self.id): []}
        if str(self.id) not in list(data.keys()):
            data.update({self.id: [roles['Роль не утсановлена']]})
            with open('data.json', 'w') as fp:
                fp.write(json.dumps(data, indent=4))

# class ChatWithGPT():
#     def __init__(self, id: int, text: str) -> None:
#         self.id = id
#         self.text = text
#         self.balance = int(check_tokens(self.id))

#     def send_to_gpt(self):
#         if len(self.text) < self.balance:
#             minus_tokens(len(self.text), self.id)
#             return main(self.id, self.text)
#         else:
#             return buy_tokens
    
class ClearHistory():
    def __init__(self, id) -> None:
        self.id = str(id)

        with open('data.json', 'r') as fp:
            data = json.load(fp)
        
        with open('data.json', 'w')  as fp:
            data[self.id].clear()
            fp.write(json.dumps(data, indent=4, ensure_ascii=False))

class AddRole():
    def __init__(self, id, role) -> None:
        self.id = id
        self.role = role
    
    def add_role(self):
        add_user_role(self.id, self.role)


from telebot import types as t
from ai import ClearData

main_kb = t.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
main_kb.add()

end_kb = t.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
btn3 = t.KeyboardButton('Закончить чат')
end_kb.add(btn3)

end_inl_chat = t.InlineKeyboardMarkup(row_width=1)
q_btn = t.InlineKeyboardButton('Сбросить чат', callback_data='Clear story')
end_inl_chat.add(q_btn)

choose_tokens = t.InlineKeyboardMarkup(row_width=1)
t_kb = t.InlineKeyboardButton('50.000💎 токенов (100 рублей)', callback_data='50k')
t_kb1 = t.InlineKeyboardButton('150.000💎💎 токенов (300 рублей)', callback_data='150k')
t_kb2 = t.InlineKeyboardButton('250.000💎💎💎 токенов (550 рублей)', callback_data='250k')
choose_tokens.add(t_kb, t_kb1, t_kb2)

roles = {'Дамблдор': 'Дамблдор', 'Программист': 'Программист', 'Шерлок Холмс': 'Шерлок Холмс', 'Эйнштейн': 'Эйнштейн', 'Пушкин': 'Пушкин', 'Маркетолог': 'Маркетолог', 'Повар': 'Повар', 'Душнила': 'Душнила', 'Сексолог': 'Сексолог', 'Лингвист': 'Лингвист', 'Психолог': 'Психолог', 'Бизнесмен': 'Бизнесмен', 'Экономист': 'Экономист'}
choose_role = t.InlineKeyboardMarkup(row_width=2)
# for k, v in roles.items():
#     choose_role.add(t.InlineKeyboardButton(text=k, callback_data=v))
r_kb = t.InlineKeyboardButton(text='Дамблдор🪄', callback_data=roles['Дамблдор'])
r_kb1 = t.InlineKeyboardButton(text='Программист👨‍💻', callback_data=roles['Программист'])
r_kb2 = t.InlineKeyboardButton(text='Шерлок Холмс🔎', callback_data=roles['Шерлок Холмс'])
r_kb3 = t.InlineKeyboardButton(text='Эйнштейн👨‍🔬', callback_data=roles['Эйнштейн'])
r_kb4 = t.InlineKeyboardButton(text='А.С. Пушкин📘', callback_data=roles['Пушкин'])
r_kb5 = t.InlineKeyboardButton(text='Маркетолог🧑‍💼', callback_data=roles['Маркетолог'])
r_kb6 = t.InlineKeyboardButton(text='Повар🧑‍🍳', callback_data=roles['Повар'])
r_kb7 = t.InlineKeyboardButton(text='Душнила🤢', callback_data=roles['Душнила'])
r_kb8 = t.InlineKeyboardButton(text='Сексолог🔞', callback_data=roles['Сексолог'])
r_kb9 = t.InlineKeyboardButton(text='Лингвист👅', callback_data=roles['Лингвист'])
r_kb10 = t.InlineKeyboardButton(text='Психолог🧠', callback_data=roles['Психолог'])
r_kb11 = t.InlineKeyboardButton(text='Бизнесмен💰', callback_data=roles['Бизнесмен'])
r_kb12 = t.InlineKeyboardButton(text='Экономист💵', callback_data='Экономист')
r_kb13 = t.InlineKeyboardButton(text='Сбросить роль', callback_data='Роль не утсановлена')
choose_role.add(r_kb, r_kb1, r_kb2, r_kb3, r_kb4, r_kb5, r_kb6, r_kb7, r_kb8, r_kb9, r_kb10, r_kb11, r_kb12, r_kb13)

from cfg import bot_token, pay_token_test, hello_mssg, info_text
from telebot import TeleBot

from user import NewUser, ClearHistory, AddRole
from keyboards import end_inl_chat, choose_tokens, choose_role
from prices import PRICE_150k, PRICE_250k, PRICE_50k
from db import user_info, update_user_status, check_user_role, last_use
from gpt_response import GptResponse

bot = TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    NewUser(message.from_user.id, message.from_user.first_name, message.from_user.username)
    bot.send_message(message.from_user.id, hello_mssg, reply_markup=None, parse_mode='HTML')

@bot.message_handler(commands=['profile'])
def profile(message):
    bot.send_message(message.from_user.id, user_info(message.from_user.id), reply_markup=None)

@bot.message_handler(commands=['buy'])
def buy(message):
    bot.send_message(message.from_user.id, 'Выбери кол-во токенов для покупки', reply_markup=choose_tokens)

@bot.message_handler(commands=['settings'])
def settings(message):
    bot.send_message(message.from_user.id, 'Выбери от чьего лица ChatGPT будет с тобой общаться', reply_markup=choose_role)

@bot.message_handler(commands=['info'])
def settings(message):
    bot.send_message(message.from_user.id, info_text, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def main(message):
    last_use(message.from_user.id)
    if check_user_role(message.from_user.id) != 'Роль не утсановлена':
        bot.send_message(message.from_user.id, f'<b>{check_user_role(message.from_user.id)}</b> думает, нужно немного подождать🤔', parse_mode="HTML")
        bot.edit_message_text(GptResponse(message.from_user.id, message.text).main(), message.from_user.id, message.message_id+1, reply_markup=end_inl_chat)
    else:
        bot.send_message(message.from_user.id, f'<b>ChatGPT</b> думает, нужно немного подождать🤔', parse_mode="HTML")
        bot.edit_message_text(GptResponse(message.from_user.id, message.text).main(), message.from_user.id, message.message_id+1, reply_markup=end_inl_chat)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                error_message="try to pay again in a few minutes, we need a small rest.")
    

@bot.message_handler(content_types=['successful_payment'])
def main_payment(message):
    print(message)
    if int(message.successful_payment.total_amount) == 10000:
        update_user_status(message.from_user.id, '💎', 50000, int(message.successful_payment.total_amount), message.successful_payment.telegram_payment_charge_id)
        bot.send_message(message.from_user.id, 'Оплата прошла успешно! Начисленно 50.000💎')
    elif int(message.successful_payment.total_amount) == 30000:
        update_user_status(message.from_user.id, '💎💎', 150000, int(message.successful_payment.total_amount), message.successful_payment.telegram_payment_charge_id)
        bot.send_message(message.from_user.id, 'Оплата прошла успешно! Начисленно 150.000💎💎')
    elif int(message.successful_payment.total_amount) == 55000:
        update_user_status(message.from_user.id, '💎💎💎', 250000, int(message.successful_payment.total_amount), message.successful_payment.telegram_payment_charge_id)
        bot.send_message(message.from_user.id, 'Оплата прошла успешно! Начисленно 250.000💎💎💎')

@bot.callback_query_handler(func=lambda call: call.data)
def main_call(call):
    if call.data == 'Clear story':
        ClearHistory(call.from_user.id)
        bot.send_message(call.from_user.id, 'Чат сброшен', reply_markup=None)

    if call.data == '50k':
        bot.send_invoice(call.from_user.id, 'Купить токены', 'После оплаты вам на счет начислится выбранное кол-во токенов', 'test-invoice-payload', provider_token=pay_token_test, prices=PRICE_50k, currency='rub')
    elif call.data == '150k':
        bot.send_invoice(call.from_user.id, 'Купить токены', 'После оплаты вам на счет начислится выбранное кол-во токенов', 'test-invoice-payload', provider_token=pay_token_test, prices=PRICE_150k, currency='rub')
    elif call.data == '250k':
        bot.send_invoice(call.from_user.id, 'Купить токены', 'После оплаты вам на счет начислится выбранное кол-во токенов', 'test-invoice-payload', provider_token=pay_token_test, prices=PRICE_250k, currency='rub')

    if call.data == 'Эйнштейн':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Дамблдор':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Шерлок Холмс':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Программист':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Пушкин':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Маркетолог':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Повар':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Душнила':
        ClearHistory(call.from_user.id) 
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Сексолог':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Лингвист':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Психолог':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Бизнесмен':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Экономист':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Выбрана роль: {call.data}! Можешь начать общение уже сейчас:)')
    elif call.data == 'Роль не утсановлена':
        ClearHistory(call.from_user.id)
        AddRole(call.from_user.id, call.data).add_role()
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f'Роль сброшена. Ты снова общаешься с GTP!')

bot.polling(skip_pending=False, none_stop=True)
        

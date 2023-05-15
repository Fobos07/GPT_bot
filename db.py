import pymysql
from cfg import db_config
from datetime import datetime

# with open('data_base.db', 'a'):
#     conn = sqlite3.Connection(r'data_base.db', check_same_thread=False)
#     cursor = conn.cursor()

conn = pymysql.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['db_name']
)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
user_id INT PRIMARY KEY,
user_name TEXT, 
user_nick TEXT, 
access_status TEXT, 
tokens BIGINT,
role TEXT
);
''')
               
cursor.execute('''
CREATE TABLE IF NOT EXISTS requests(
user_id INT PRIMARY KEY,
request_data TEXT
);
''')
               
cursor.execute('''
CREATE TABLE IF NOT EXISTS perchases(
user_id BIGINT,
date TEXT,
sum INT,
pay_id TEXT,
last_using TEXT
);
''')

def add_user(data):
    cursor.execute('INSERT IGNORE INTO users VALUES(%s, %s, %s, %s, %s, %s, %s);', data)
    conn.commit()


def response_data(id):
    cursor.execute('SELECT request_data FROM requests WHERE user_id = %s;', (id,))
    return cursor.fetchall()[0][0]

def add_new_request(data, id):
    cursor.execute('UPDATE requests SET request_data = %s WHERE user_id = %s;', (str(data), id))
    conn.commit()

def user_info(id):
    cursor.execute('SELECT * FROM users WHERE user_id = %s;', (id,))
    user_information = cursor.fetchall()[0]
    tokens = user_information[4]
    if user_information[5] == None:
        role = 'Роль не выбрана'
    else:
        role = user_information[5]
    if int(tokens) < 0:
        cursor.execute('UPDATE users SET tokens = 0 WHERE user_id = %s;', (id,))
        conn.commit() 
        tokens = 0
    conn.commit()
    return (
        f'''id: {user_information[0]}
Имя пользователя: {user_information[1]}
Доступные токены: {tokens}
Статус подписки: {user_information[3]}
Выбранная роль: {role}
''')

def add_purch(id, summ, pay_id):
    cursor.execute('INSERT INTO perchases VALUES(%s, %s, %s, %s);', (id, str(datetime.today()), summ//100, pay_id))
    conn.commit()

def update_user_status(id, status, tokens, summ, pay_id):
    cursor.execute('UPDATE users SET access_status = %s, tokens = tokens + %s WHERE user_id = %s;', (status, tokens, id,))
    conn.commit()
    add_purch(id, summ, pay_id)

def minus_tokens(length, id):
    cursor.execute('UPDATE users SET tokens = tokens - %s WHERE user_id = %s;', (length, id,))
    conn.commit()

def check_tokens(id):
    cursor.execute('SELECT tokens FROM users WHERE user_id = %s;', (id,))
    return cursor.fetchall()[0][0]

def add_user_role(id, role):
    cursor.execute('UPDATE users SET role = %s WHERE user_id = %s;', (role, id,))
    conn.commit()

def check_user_role(id):
    cursor.execute('SELECT role FROM users WHERE user_id = %s;', (id,))
    return cursor.fetchall()[0][0]

def last_use(id):
    cursor.execute('UPDATE users SET last_using = %s WHERE user_id = %s;', (str(datetime.today()), id,))
    conn.commit()


# Добавление столбца в таблицу
def add_new_column():
    cursor.execute('ALTER TABLE users ADD PRIMARY KEY (user_id);')
    conn.commit()
# add_new_column()

# Удаление столбца из таблицы
def test():
    cursor.execute('''ALTER TABLE perchases DROP COLUMN last_using;''')
    conn.commit()
# test()
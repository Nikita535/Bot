import sqlite3 as sq
from create_bot import bot

def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT,name TEXT PRIMARY KEY,description TEXT, price TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS admins(name TEXT ,id INT PRIMARY KEY)')
    base.commit()

async def sql_add_admin(message):
    cur.execute('INSERT INTO admins VALUES (?,?)', (message.from_user.username, message.from_user.id))
    base.commit()

async def sql_show_admins():
    return cur.execute('SELECT * FROM admins').fetchall()

async def sql_show_admin_by_id(message):
    return cur.execute('SELECT id FROM admins WHERE name==?',(message.from_user.username,)).fetchone()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)',tuple(data.values()))
        base.commit()

async def sql_read(message):
    if len(cur.execute('SELECT * FROM menu').fetchall())==0:
       await bot.send_message(message.from_user.id,'Меню пустое')
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()



async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
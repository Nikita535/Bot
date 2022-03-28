import sqlite3 as sq
from create_bot import bot
import json
def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT ,img TEXT PRIMARY KEY , price TEXT)')
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
        cur.execute('INSERT INTO menu VALUES (?,?,?)',tuple(data.values()))
        base.commit()

def sql_add_from_json():
    with open('./ParserMenu/menu_dict.json', encoding="utf-8") as file:
        menu_dict = json.load(file)
        for k, v in menu_dict.items():
            item = cur.execute('SELECT img FROM menu WHERE img==?',(str(v['photo_name']),)).fetchone()
            if item == None:
                cur.execute('INSERT INTO menu VALUES (?,?,?)',(str(v['name']),str(v['photo_name']),str(v['price'])))
    base.commit()
async def sql_read(message):
    if len(cur.execute('SELECT * FROM menu').fetchall())==0:
       await bot.send_message(message.from_user.id,'Меню пустое')
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        if str(ret[1]).find('.')!=-1 :
            photopath = open("./ParserMenu/pics/" + ret[1], 'rb')
        else:
            photopath = ret[1]
        await bot.send_photo(message.from_user.id, photopath, f'{ret[0]}\nЦена {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()



async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE img == ?', (data,))
    base.commit()


async def sql_test():
    return cur.execute("SELECT * FROM menu WHERE name==?",('/Удалить',)).fetchone()
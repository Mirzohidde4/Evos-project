import sqlite3, logging


def sql_connect():
    try:
        connection = sqlite3.connect("../db.sqlite3")  # SQLite3 bazasiga bog'lanish
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False


def sql_connection():
    connection = sqlite3.connect("../db.sqlite3")  # SQLite3 bazasiga bog'lanish
    connection.commit()
    return connection


def ReadDb(id):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {id}")

        res = cursor.fetchall()
        conn.commit()
        l = list()
        if not res:
            return False
        else:
            for i in res:
                l.append(i)
            return l
    else:
        return False
    

def AddXabar(author, author_id, username, text):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO main_xabarlar (author, author_id, username, text) VALUES (?, ?, ?, ?)""",
                (author, author_id, username, text),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False    


def AddUser(user_id, fullname, username, phone):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO main_users (user_id, fullname, username, phone) VALUES (?, ?, ?, ?)""",
                (user_id, fullname, username, phone),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False    
    
    
def AddSavat(user, user_id, name, count, price, total_price):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO main_savat (user, user_id, name, count, price, total_price) VALUES (?, ?, ?, ?, ?, ?)""",
                (user, user_id, name, count, price, total_price),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False   


def AddBuyurtma(user, user_id, name, count, price, total_price, created, turi, status):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO main_buyurtmalar (user, user_id, name, count, price, total_price, created, pay, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user, user_id, name, count, price, total_price, created, turi, status),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False   


def DeleteDb(table, key, value):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE {key} = {value}")
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def UpdateSavat(count, total_price, user_id, name):
    try:
        with sqlite3.connect("../db.sqlite3") as con:
            cur = con.cursor()
            cur.execute("UPDATE main_savat SET (count, total_price) = (?, ?) WHERE (user_id, name) = (?, ?)", (count, total_price, user_id, name))
            con.commit()
            print(f"Updated Product: {name} with count: {count}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def UpdateBuyurtma(user_id, created, status):
    try:
        with sqlite3.connect("../db.sqlite3") as con:
            cur = con.cursor()
            cur.execute("UPDATE main_buyurtmalar SET (status) = (?) WHERE (user_id, created) = (?, ?)", (status, user_id, created))
            con.commit()
            print(f"Updated Product: {user_id} with status: {status}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def Taomlarr(category):
    menyu_id = 0
    if ReadDb('main_menyu'):
        for menyu in ReadDb('main_menyu'):
            if menyu[1] == category:
                menyu_id = menyu[0]
                break
    else:
        return False        
    
    if ReadDb('main_food'):
        taomlar = []
        for taom in ReadDb('main_food'):
            if taom[3] == menyu_id:
                taomlar.append(taom[1])
        return taomlar        
    else:
        return False


def Mahsulotlar(product):
    if ReadDb('main_food'):
        action = []
        for mahsulot in ReadDb('main_food'):
            if mahsulot[1] == product:
                action.append(mahsulot[2])
                action.append(mahsulot[4])
                action.append(mahsulot[5])
                action.append(mahsulot[6])
                break
        return action
    else:
        return False


def Tasdiqlanmagan(id):
    tasdiqlanmaganlar = 0
    if ReadDb('main_savat'):
        for user in ReadDb('main_savat'):
            if user[2] == id:
                tasdiqlanmaganlar += 1
    
    return [tasdiqlanmaganlar if tasdiqlanmaganlar else False]


def Tozalash(dtb, bolim, user_id):
    if ReadDb(dtb):
        for user in ReadDb(dtb):
            if (dtb == 'main_users') and (user[1] == user_id):
                try:
                    DeleteDb(dtb, bolim, user_id)
                except Exception as e:
                    print(f'malumot o\'chirilmadi: {e}')
            
            elif user[2] == user_id:
                try:
                    DeleteDb(dtb, bolim, user_id)
                except Exception as e:
                    print(f'malumot o\'chirilmadi: {e}')


def Zakaz(user_id):
    if ReadDb('main_buyurtmalar'):
        prices = []
        response = str('\n\n🍱 <b>Sizning buyurtmangiz:</b>')
        for user in ReadDb('main_buyurtmalar'):
            if user[3] == user_id:
                response += str(f'\n       <b>{user[4]}</b> - {user[5]} ta')   
                prices.append(user[7])
                tur = user[8]
                date = user[1]
        total_prices = sum(prices)

        if tur == 'naqd':
            text=f"📦 <b>Buyurtmangiz holati:</b> aktiv{response}\n<b>💵 Umumiy narx:</b> {total_prices:.2f} so\'m\n📌 <b>Buyurtma berilgan sana:</b> {date}\n💳 <b>To'lov turi: </b>{tur}\n\n🚛 <b>Buyurtma 15-20 daqiqa ichida oldingizda bo\'ladi ✅</b>"
            return text
        elif tur == 'karta':
            text=f"📦 <b>Buyurtmangiz holati:</b> aktiv emas{response}\n<b>💵 Umumiy narx:</b> {total_prices:.2f} so\'m\n📌 <b>Buyurtma berilgan sana:</b> {date}\n💳 <b>To'lov turi: </b>{tur}\n\n🚛 <b>Buyurtma to\'lovni amalga oshirganingizdan keyin yo\'lga chiqadi.</b>"
            return text

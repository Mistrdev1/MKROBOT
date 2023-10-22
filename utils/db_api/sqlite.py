import sqlite3
from unittest import result


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

# ----------------- Firdavs Programmer ---------------------- #

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

# ----------------- Firdavs Programmer ---------------------- #

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

# ----------------- Firdavs Programmer ---------------------- #
# Users jadvali bilan ishlash
    # Foydalanuvchi qo'shish
    def add_user(self, user_id, username, status, linked_id, balans, subscription, subscription_off):
        return self.execute("INSERT INTO Users(user_id, username, status, linked_id, balans, subscription, subscription_off) VALUES(?, ?, ?, ?, ?, ?, ?)", (user_id, username, status, linked_id, balans, subscription, subscription_off), commit=True)

    def add_user_datas(self, user_fullname, phone, user_id):
        return self.execute("UPDATE Users SET user_fullname=?, phone=? WHERE user_id=?", (user_fullname, phone, user_id), commit=True)

    # admin qo'shish
    def add_admin(self, admin_id, admins, channels, send_post, admin_post):
        return self.execute("INSERT INTO admins(admin_id, admins, channels, send_post, admin_post) VALUES(?, ?, ?, ?, ?)", (admin_id, admins, channels, send_post, admin_post), commit=True)

    # majburiy azolik uchun kanal qo'shish
    def add_channel(self, name, channel_id):
        return self.execute("INSERT INTO kanallar(name, channel_id) VALUES(?,?)", (name, channel_id), commit=True)

    # Hamma foydalanuvchilarning id raqamini olish
    def id_users(self):
        return self.execute("SELECT user_id FROM Users", fetchall=True)

    # Hamma foydalanuvchilarni belgilab ular haqida malumot olish
    def select_all_users(self):
        return self.execute("SELECT * FROM Users", fetchall=True)

    # Foydalanuvchini tekshirish bazada bor yoki yo'qligini
    def check_user(self, user_id):
        return self.execute("SELECT user_id FROM Users WHERE user_id=?", (user_id,), fetchall=True)

    def check_subscription(self, user_id):
        return self.execute("SELECT subscription FROM Users WHERE user_id=?", (user_id,), fetchone=True)

    def get_userbalans(self, user_id):
        return self.execute("SELECT balans FROM Users WHERE user_id=?", (user_id,), fetchone=True)

    def update_balans(self, balans, user_id):
        return self.execute("UPDATE Users SET balans=? WHERE user_id=?", (balans, user_id,), commit=True)

    def get_user_name(self, user_id):
        return self.execute("SELECT user_fullname FROM Users WHERE user_id=?", (user_id,), fetchone=True)

    # Check Admin
    def check_admin(self, admin_id):
        return self.execute("SELECT admin_id FROM admins WHERE admin_id=?", (admin_id,), fetchone=True)

    # user_id bilan foydalanuvchilarning ma'lumotlarini olish
    def select_user_datas(self, user_id):
        return self.execute("SELECT * FROM Users WHERE user_id=?", (user_id,), fetchone=True)

    # kanalni tekshirish
    def check_channel(self, channel_id):
        return self.execute("SELECT channel_id FROM kanallar WHERE channel_id=?", (channel_id,), fetchone=True)

    # hamma kanallarni olish
    def select_channels(self):
        return self.execute("SELECT * FROM kanallar WHERE TRUE", fetchall=True)

    # user_id bilan adminlarning statusini olish
    def get_admins(self, user_id):
        return self.execute("SELECT status FROM Users WHERE user_id=?", (user_id,), fetchone=True)

    # hamma adminlarning barcha ma'lumotlarini olish uchun funksiya
    def select_all_admins(self, status):
        return self.execute("SELECT * FROM Users WHERE status=?", (status,), fetchall=True)

    # hamma adminlarning user_id sini olish uchun funksiyasi
    def select_all_admins_user_ids(self, status):
        return self.execute("SELECT user_id FROM Users WHERE status=?", (status,), fetchall=True)

    # foydalanuvchining statusini yangilash uchun funksiyasi
    def update_status(self, status, user_id):
        return self.execute("UPDATE Users SET status=? WHERE user_id=?", (status, user_id,), commit=True)

    # Bazadagi foydalanuvchilarni sanash
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users", fetchone=True)

    # admin uchun adminlar ruhsatlarini olish
    def get_admin_rights(self, admin_id):
        return self.execute("SELECT * FROM admins WHERE admin_id=?", (admin_id,), fetchone=True)

    # kanalni o'chirish funksiyasi
    def delete_channel(self, id):
        return self.execute("DELETE FROM kanallar WHERE id=?", (id,), commit=True)

    # Adminni o'chirish
    def delete_admin(self, admin_id):
        return self.execute("DELETE FROM admins WHERE admin_id=?", (admin_id,), commit=True)
    
    def delete_user(self, user_id):
        return self.execute("DELETE FROM Users WHERE user_id=?", (user_id,), commit=True)

    # Users jadvalidagi barcha malumotlarni tozalash
    def delete_all_users(self):
        return self.execute("DELETE FROM Users WHERE TRUE", commit=True)

# Adminlarning ruhsatlarini yangilash funksiyalari
    # Admin uchun adminlar bo'lini almashtirish uchun funksiyasi
    def update_admin_admin(self, admins, admin_id):
        return self.execute("UPDATE admins SET admins=? WHERE admin_id=?", (admins, admin_id,), commit=True)

    # Admin uchun kanallar bo'limini almashtirish uchun  funksiyasi
    def update_admin_channels(self, channels, admin_id):
        return self.execute("UPDATE admins SET channels=? WHERE admin_id=?", (channels, admin_id,), commit=True)

    # admin uchun reklama yuborish funksiyasi
    def update_admin_send_post(self, send_post, admin_id):
        return self.execute("UPDATE admins SET send_post=? WHERE admin_id=?", (send_post, admin_id,), commit=True)

    # admin uchun adminlarga reklama yuborish funksiyasi
    def update_admin_admin_post(self, admin_post, admin_id):
        return self.execute("UPDATE admins SET admin_post=? WHERE admin_id=?", (admin_post, admin_id,), commit=True)

    def update_user_subs(self, subscription, user_id):
        return self.execute("UPDATE users SET subscription=? WHERE user_id=?", (subscription, user_id,), commit=True)

    def update_user_subs_date(self, subscription_on, user_id):
        return self.execute("UPDATE users SET subscription_on=? WHERE user_id=?", (subscription_on, user_id,), commit=True)

    def select_users_subscription(self, subscription):
        return self.execute("SELECT * FROM Users WHERE subscription=?", (subscription,), fetchall=True)

    def get_user_subs(self, user_id):
        return self.execute("SELECT subscription FROM users WHERE user_id=?", (user_id,), fetchone=True)

    def update_subs_month(self, subs_month, user_id):
        return self.execute("UPDATE users SET subs_month=? WHERE user_id=?", (subs_month, user_id), commit=True)

    def get_subs_month(self, user_id):
        return self.execute("SELECT subs_month FROM users WHERE user_id=?", (user_id,), fetchone=True)

    def update_subscription_off(self, subscription_off, user_id):
        return self.execute("UPDATE users SET subscription_off=? WHERE user_id=?", (subscription_off, user_id,), commit=True)

    def get_month(self, id):
        return self.execute("SELECT * FROM prices WHERE id=?", (id,), fetchone=True)

    def get_payment(self, name):
        return self.execute("SELECT * FROM payments WHERE name=?", (name,), fetchone=True)

    def get_price(self, id):
        return self.execute("SELECT * FROM prices WHERE id=?", (id,), fetchone=True)

    def get_userbalans(self, user_id):
        return self.execute("SELECT balans FROM Users WHERE user_id=?", (user_id,), fetchone=True)

    def get_invited(self, linked_id):
        return self.execute("SELECT linked_id FROM Users WHERE linked_id=?", (linked_id,), fetchall=True)

    def get_notification_status(self, user_id, subscription):
        return self.execute("SELECT trade_notification FROM Users WHERE user_id=? AND subscription=?", (user_id, subscription,), fetchone=True)

    def get_all_users_notif_status(self, trade_notification):
        return self.execute("SELECT user_id FROM Users WHERE trade_notification=?", (trade_notification,), fetchall=True)

    def update_notification_status(self, trade_notification, user_id):
        return self.execute("UPDATE Users SET trade_notification=? WHERE user_id=?", (trade_notification, user_id), commit=True)


    def select_user_info(self, user_id):
        return self.execute("SELECT * FROM users WHERE user_id=?", (user_id,), fetchone=True)
    
# BIRJA

    def update_birja(self, birja, user_id):
        return self.execute("UPDATE Users SET birja=? WHERE user_id=?", (birja, user_id), commit=True)


################# =-=-=-=-=-=-=-=-= ################
# OBMEN FUNCTIONS
# Obmen uchun funksiyalar

    def add_transfer(self, user_id, exchange, updated_time, status, summa):
        return self.execute("INSERT INTO transfers(user_id, exchange, updated_time, status, summa) VALUES(?, ?, ?, ?, ?)", (user_id, exchange, updated_time, status, summa,), commit=True)

    def get_transfer_data(self, user_id):
        return self.execute("SELECT * FROM transfers WHERE user_id=?", (user_id,), fetchone=True)


# ZAHIRA 

    def update_zahira_usdt(self, usdt, id):
        return self.execute("UPDATE zahira SET usdt=? WHERE id=?", (usdt, id,), commit=True)

    def update_zahira_som(self, som, id):
        return self.execute("UPDATE zahira SET som=? WHERE id=?", (som, id,), commit=True)


    def get_zahira(self, id):
        return self.execute("SELECT * FROM zahira WHERE id=?", (id,), fetchone=True)
# TESTLAR

    def update_test(self, test, user_id):
        return self.execute("UPDATE users SET test = ? WHERE user_id=?", (test, user_id), commit=True)
    
    def select_test(self, id):
        result = self.execute("SELECT * FROM testlar WHERE id=?", (id,), fetchall=True)
        return result


# KURSLAR

    def update_kurs_olish(self, olish, id):
        return self.execute("UPDATE kurslar SET olish=? WHERE id=?", (olish, id,), commit=True)

    def update_kurs_sotish(self, sotish, id):
        return self.execute("UPDATE kurslar SET sotish=? WHERE id=?", (sotish, id,), commit=True)


    def get_kurs(self, id):
        return self.execute("SELECT * FROM kurslar WHERE id=?", (id,), fetchone=True)


# Valyutalar

    def add_valyuta(self, user_id, Binance, HuobiGlobal, Bybit, OKX):
        return self.execute("INSERT INTO valyutalar(user_id, Binance, HuobiGlobal, Bybit, OKX) VALUES(?, ?, ?, ?, ?)", (user_id, Binance, HuobiGlobal, Bybit, OKX), commit=True)

    def check_user_valyuta(self, user_id):
        return self.execute("SELECT user_id FROM valyutalar WHERE user_id=?", (user_id,), fetchone=True)
    
    def binance_update(self, Binance, user_id):
        return self.execute("UPDATE valyutalar SET Binance=? WHERE user_id=?", (Binance, user_id), commit=True)

    def HuobiGlobal_update(self, HuobiGlobal, user_id):
        return self.execute("UPDATE valyutalar SET HuobiGlobal=? WHERE user_id=?", (HuobiGlobal, user_id), commit=True)

    def Bybit_update(self, Bybit, user_id):
        return self.execute("UPDATE valyutalar SET Bybit=? WHERE user_id=?", (Bybit, user_id), commit=True)

    def OKX_update(self, OKX, user_id):
        return self.execute("UPDATE valyutalar SET OKX=? WHERE user_id=?", (OKX, user_id), commit=True)

    def select_user_valyuta(self, user_id):
        return self.execute("SELECT * FROM valyutalar WHERE user_id=?", (user_id,), fetchone=True)
    


# Copy Trade

    def add_trader(self, user_id, name):
        return self.execute("INSERT INTO traders(user_id, name) VALUES(?, ?)", (user_id, name), commit=True)

    def select_trader(self, name):
        return self.execute("SELECT * FROM traders WHERE name=?", (name,), fetchall=True)
    
    def check_trader(self, user_id, name):
        return self.execute("SELECT * FROM traders WHERE user_id=? AND name=?", (user_id, name), fetchall=True)
        
    def delete_trader(self, user_id, name):
        return self.execute("DELETE FROM traders WHERE user_id=? AND name=?", (user_id, name), commit=True)


def logger(statement):
    print(f"Executing: {statement}")

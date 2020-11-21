import mysql.connector
import json
from os import path


DB_INFO = "constants/database.json"

class Data_accessor(object):
 
    def __init__(self):
        parent_dir = path.dirname(path.abspath(__file__))
        with open(f"{parent_dir}/../{DB_INFO}") as json_data:
            db_info = json.load(json_data)["mysql"]
        self.connector = mysql.connector.connect(user=db_info["user"], password=db_info["password"],
                                                 host=db_info["host"], database=db_info["database"])

    def create_user(self, name, password):
        try:
            cursor = self.connector.cursor()
            query = """
                    INSERT INTO users
                    (login, password)
                    VALUES (%(login)s, %(password)s)
                    """
            cursor.execute(query, {"login": name, "password": password})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def user_exist(self, name):
        try:
            cursor = self.connector.cursor(dictionary=True)
            query = """
                    SELECT login
                    FROM users
                    WHERE login=%(login)s
                    """
            cursor.execute(query, {"login": name})
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                return False
            return True
        except:
            return True

    def create_chat(self, user_name, chat_name):
        try:
            cursor = self.connector.cursor()
            query = """
                    INSERT INTO chats
                    (chat_name, owner)
                    VALUES (%(chat_name)s, %(owner)s)
                    """
            cursor.execute(query, {"chat_name": chat_name, "owner": user_name})
            id = cursor.lastrowid
            self.connector.commit()
            cursor.close()
            return id
        except:
            return None

    def join_chat(self, chat_id, user):
        try:
            cursor = self.connector.cursor()
            query = """
                    INSERT INTO chats_users
                    (chat_id, login)
                    VALUES (%(chat_id)s, %(user)s)
                    """
            cursor.execute(query, {"chat_id": chat_id, "user": user})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def create_chat_notifications(self, user, chat_id):
        try:
            cursor = self.connector.cursor()
            query = """
                    INSERT INTO chats_users_notifications
                    (chat_id, login)
                    VALUES (%(chat_id)s, %(user)s)
                    """
            cursor.execute(query, {"chat_id": chat_id, "user": user})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def get_chat_notifications(self, user):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    SELECT chat_id
                    FROM chats_users_notifications
                    WHERE login=%(login)s
                    """
            cursor.execute(query, {"login": user})
            result = []
            for (number) in cursor:
                result.append(*number)
            cursor.close()
            return result
        except:
            return None

    def delete_chat_notification(self, user, chat_number):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    DELETE
                    FROM chats_users_notifications
                    WHERE chat_id=%(chat_id)s AND login=%(login)s
                    """
            cursor.execute(query, {"login": user, "chat_id": chat_number})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def chat_owner(self, chat_number):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    SELECT owner
                    FROM chats
                    WHERE id=%(id)s
                    """
            cursor.execute(query, {"id": chat_number})
            result = []
            for (owner) in cursor:
                result.append(*owner)
            if len(result) == 0:
                return None
            else:
                return result[0]
            cursor.close()
            return result
        except:
            return None

    def leave_chat(self, user, chat_id):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    DELETE
                    FROM chats_users
                    WHERE chat_id=%(chat_id)s AND login=%(login)s
                    """
            cursor.execute(query, {"login": user, "chat_id": chat_id})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def chat_name(self, chat_number):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    SELECT chat_name
                    FROM chats
                    WHERE id=%(id)s
                    """
            cursor.execute(query, {"id": chat_number})
            result = []
            for (owner) in cursor:
                result.append(*owner)
            cursor.close()
            if len(result) == 0:
                return None
            else:
                return result[0]
        except:
            return None

    def delete_chat(self, chat_id):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    DELETE
                    FROM chats
                    WHERE id=%(chat_id)s
                    """
            cursor.execute(query, {"chat_id": chat_id})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def check_password(self, user_name, password):
        try:
            cursor = self.connector.cursor(dictionary=True)
            query = """
                    SELECT login
                    FROM users
                    WHERE login=%(login)s and password=%(password)s
                    """
            cursor.execute(query, {"login": user_name, "password": password})
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                return False
            return True
        except:
            return False

    def change_password(self, user_name, password):
        try:
            cursor = self.connector.cursor(dictionary=True)
            query = """
                    UPDATE users
                    SET password = %(password)s
                    WHERE login=%(login)s
                    """
            cursor.execute(query, {"login": user_name, "password": password})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def all_users_in_chat(self, chat_number):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    SELECT login
                    FROM chats_users
                    WHERE chat_id=%(id)s
                    """
            cursor.execute(query, {"id": chat_number})
            result = []
            for (login) in cursor:
                result.append(*login)
            cursor.close()
            return result
        except:
            return None

    def all_chats_for_user(self, user_name):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    SELECT chat_id
                    FROM chats_users
                    WHERE login=%(login)s
                    """
            cursor.execute(query, {"login": user_name})
            result = []
            for (num) in cursor:
                result.append(*num)
            cursor.close()
            return result
        except:
            return None

    def create_message_notification(self, chat_id, users_names):
        try:
            for user in users_names:
                cursor = self.connector.cursor()
                query = """
                        INSERT INTO messages_users_notifications
                        (chat_id, login)
                        VALUES (%(chat_id)s, %(user)s)
                        """
                cursor.execute(query, {"chat_id": chat_id, "user": user})
                self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def send_message(self, user_name, chat_id, message):
        try:
            cursor = self.connector.cursor()
            query = """
                    INSERT INTO messages
                    (chat_id, login, message)
                    VALUES (%(chat_id)s, %(user)s, %(message)s)
                    """
            cursor.execute(query, {"chat_id": chat_id, "user": user_name, "message": message})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False

    def list_messages(self, chat_number):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    SELECT login, message
                    FROM messages
                    WHERE chat_id=%(chat_id)s
                    """
            cursor.execute(query, {"chat_id": chat_number})
            result = []
            for (user, message) in cursor:
                result.append({"user": user, "messge": message})
            cursor.close()
            return result
        except:
            return None

    def get_messages_notifications(self, user):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    SELECT chat_id
                    FROM messages_users_notifications
                    WHERE login=%(login)s
                    """
            cursor.execute(query, {"login": user})
            result = []
            for (number) in cursor:
                result.append(*number)
            cursor.close()
            return result
        except:
            return None

    def delete_message_notification(self, user, chat_number):
        try:
            cursor = self.connector.cursor(buffered=True)
            query = """
                    DELETE
                    FROM messages_users_notifications
                    WHERE chat_id=%(chat_id)s AND login=%(login)s
                    """
            cursor.execute(query, {"login": user, "chat_id": chat_number})
            self.connector.commit()
            cursor.close()
            return True
        except:
            return False


from . import response
from .data_accessor import Data_accessor


data_accessor = Data_accessor()

def main():
    return response.response(200, "Server API for Simple Messenger")

# Логин/пароль 60 символов
def create_user(name, password):
    if name is None or password is None:
        return response.response(400, "Need user and password")
    if data_accessor.user_exist(name):
        return response.response(400, f"User with name {name} already exist")
    if data_accessor.create_user(name, password):
        return response.response(200, f"User with name {name} created")
    else:
        return response.response(500, f"Failed to create a user with the name {name}")

def create_chat(user_name, chat_name):
    if user_name is None or chat_name is None:
        return response.response(400, "Need user and chat_number")
    create_result = data_accessor.create_chat(user_name, chat_name)
    if create_result is None:
        return response.response(500, f"Failed to create a chat with the name {chat_name}")
    if data_accessor.join_chat(create_result, user_name):
        return response.response(200, f"Chat with name {chat_name} created", sensible=create_result)
    return response.response(500, f"Failed join to chat with the name {chat_name}")

# Можно инвайтить уже присмоединенных пользователей
def invite_user(user_name, chat_number):
    if user_name is None or chat_number is None:
        return response.response(400, "Need user and chat_number")
    if data_accessor.create_chat_notifications(user_name, chat_number):
        return response.response(200, f"User {user_name} invited")
    return response.response(500, f"Failed to invite a user with the name {user_name}." +
                                    " User already invited or user/chat don't exist.")

def get_chat_notifications(user_name):
    if user_name is None:
        return response.response(400, "Need user")
    result = data_accessor.get_chat_notifications(user_name)
    if result:
        return response.response(200, f"Chats information for a user with the name {user_name}", sensible=result)
    return response.response(500, f"Failed to get information for a user with the name {user_name}")

def delete_chat_notification(user_name, chat_number):
    if user_name is None or chat_number is None:
        return response.response(400, "Need user and chat_number")
    if data_accessor.delete_chat_notification(user_name, chat_number):
        return response.response(200, f"Notification delete for a user with the name {user_name}")
    return response.response(500, f"Failed to delete notification for a user with the name {user_name}")

# Возможно нужна проверка на сущестование уведомления
def join_chat(user_name, chat_number):
    if user_name is None or chat_number is None:
        return response.response(400, "Need user and chat_number")
    if not data_accessor.delete_chat_notification(user_name, chat_number):
        return response.response(500, f"Failed to delete notification for a user with the name {user_name}")
    if data_accessor.join_chat(chat_number, user_name):
        return response.response(200, f"Join to chat with id {chat_number}")
    return response.response(500, f"Failed join to chat with id {chat_number}")

def chat_owner(chat_number):
    if chat_number is None:
        return response.response(400, "Need chat_number")
    result = data_accessor.chat_owner(chat_number)
    if result is None:
        return response.response(400, f"Chat {chat_number} not exist")
    return response.response(200, f"Owner for chat {chat_number}", sensible=result)

def leave_chat(user_name, chat_number):
    if user_name is None or chat_number is None:
        return response.response(400, "Need user and chat_number")
    if user_name == data_accessor.chat_owner(chat_number):
        return response.response(400, f"Chat owner can not leave chat {chat_number}")
    if data_accessor.leave_chat(user_name, chat_number):
        return response.response(200, f"Leave from chat {chat_number}")
    else:
        return response.response(500, f"Failed leave chat with id {chat_number}")

def chat_name(chat_number):
    if chat_number is None:
        return response.response(400, "Need chat_number")
    result  = data_accessor.chat_name(chat_number)
    if result is None:
        return response.response(400, f"Chat with number {chat_number} don't exist")
    return response.response(200, f"Chat with number {chat_number} exist", sensible=result)

def delete_chat(user_name, chat_number):
    if user_name is None or chat_number is None:
        return response.response(400, "Need user and chat_number")
    if not user_name == data_accessor.chat_owner(chat_number):
        return response.response(400, f"User with the name {user_name} are not chat owner for {chat_number}")
    if data_accessor.delete_chat(chat_number):
        return response.response(200, f"Delete chat {chat_number}")
    else:
        return response.response(500, f"Failed to delete chat with id {chat_number}")

def check_password(user_name, password):
    if user_name is None or password is None:
        return response.response(400, "Need user and password")
    if data_accessor.check_password(user_name, password):
        return response.response(200, f"Password for user {user_name} coorect", sensible=True)
    else:
        return response.response(400, f"Password for user {user_name} incoorect", sensible=False)

# Если прользователя нет, то все пройдет успешно
def change_password(user_name, password):
    if user_name is None or password is None:
        return response.response(400, "Need user and password")
    if data_accessor.change_password(user_name, password):
        return response.response(200, f"Password for user {user_name} changed")
    else:
        return response.response(500, f"User with name {user_name} not exist")

# Если чата нет, то верент пустой лист
def all_users_in_chat(chat_number):
    if chat_number is None:
        return response.response(400, "Need chat_number")
    result = data_accessor.all_users_in_chat(chat_number)
    if result is None:
        return response.response(500, f"Failed take list all users for chat with id {chat_number}")
    return response.response(200, f"List all users for chat with id {chat_number}", sensible=result)

def all_chats_for_user(user_name):
    if user_name is None:
        return response.response(400, "Need user")
    result = data_accessor.all_chats_for_user(user_name)
    if result is None:
        return response.response(500, f"Failed take list all chats for user with name {user_name}")
    return response.response(200, f"List all chats for user with name {user_name}", sensible=result)

def send_message(user_name, chat_number, message):
    if user_name is None or chat_number is None or message is None:
        return response.response(400, "Need user, chat_number, message")
    if data_accessor.send_message(user_name, chat_number, message):
        users_name = data_accessor.all_users_in_chat(chat_number)
        if users_name is None:
            return response.response(500, f"Failed take list all users for chat with id {chat_number}")
        users_name.remove(user_name)
        data_accessor.create_message_notification(chat_number, users_name)
        return response.response(200, f"Message from {user_name} sended")
    return response.response(400, f"Message from {user_name} not sended")

def list_messages(chat_number):
    if chat_number is None:
        return response.response(400, "Need chat_number")
    result = data_accessor.list_messages(chat_number)
    if result is None:
        return response.response(500, f"Failed get list to the chat with id {chat_number}")
    return response.response(200, f"List all messages for the chat with id {chat_number}", sensible=result)

def get_messages_notifications(user_name):
    if user_name is None:
        return response.response(400, "Need user")
    result = data_accessor.get_messages_notifications(user_name)
    if result:
        return response.response(200, f"Chats information for a user with the name {user_name}", sensible=result)
    return response.response(500, f"Failed to get information for a user with the name {user_name}")

def delete_message_notification(user_name, chat_number):
    if user_name is None or chat_number is None:
        return response.response(400, "Need user and chat_number")
    if data_accessor.delete_message_notification(user_name, chat_number):
        return response.response(200, f"Notification delete for a user with the name {user_name}")
    return response.response(500, f"Failed to delete notification for a user with the name {user_name}")

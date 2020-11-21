#!/usr/bin/env python3

from flask import Flask
from flask import request
from core import api

app = Flask(__name__)


@app.route('/')
def main():
    return api.main()

# /create_user?user_name=NAME&password=PASSWORD
@app.route('/create_user')
def create_user():
    return api.create_user(request.args.get('user_name', type=str), request.args.get('password', type=str))

# /create_chat?user_name=USER&chat_name=CHAT
# return int chat id
@app.route('/create_chat')
def create_chat():
    return api.create_chat(request.args.get('user_name', type=str), request.args.get('chat_name', type=str))

# /chat_name?chat_number=1
# return str chat name
@app.route('/chat_name')
def chat_name():
    return api.chat_name(request.args.get('chat_number', type=int))

# /chat_owner?chat_number=1
# return str owner for the chat
@app.route('/chat_owner')
def get_chat_owner():
    return api.chat_owner(request.args.get('chat_number', type=int))

# /invite_user?user_name=USER&chat_number=1
@app.route('/invite_user')
def invite_user():
    return api.invite_user(request.args.get('user_name', type=str), request.args.get('chat_number', type=int))

# /get_chat_notifications?user_name=USER
# return list chat notifications
@app.route('/get_chat_notifications')
def get_chat_notifications():
    return api.get_chat_notifications(request.args.get('user_name', type=str))

# /delete_chat_notification?user_name=USER&chat_number=1
@app.route('/delete_chat_notification')
def delete_chat_notification():
    return api.delete_chat_notification(request.args.get('user_name', type=str), request.args.get('chat_number', type=int))

# /join_chat?user_name=USER&chat_number=1
@app.route('/join_chat')
def join_chat():
    return api.join_chat(request.args.get('user_name', type=str), request.args.get('chat_number', type=int))

# /leave_chat?user_name=USER&chat_number=1
@app.route('/leave_chat')
def leave_chat():
    return api.leave_chat(request.args.get('user_name', type=str), request.args.get('chat_number', type=int))

# /delete_chat?user_name=USER&chat_number=1
@app.route('/delete_chat')
def delete_chat():
    return api.delete_chat(request.args.get('user_name', type=str), request.args.get('chat_number', type=int))

# /check_password?user_name=NAME&password=PASSWORD
# return bool
@app.route('/check_password')
def check_password():
    return api.check_password(request.args.get('user_name', type=str), request.args.get('password', type=str))

# /change_password?user_name=NAME&password=PASSWORD
@app.route('/change_password')
def change_password():
    return api.change_password(request.args.get('user_name', type=str), request.args.get('password', type=str))

# /all_users_in_chat?chat_number=1
# return list logins
@app.route('/all_users_in_chat')
def all_users_in_chat():
    return api.all_users_in_chat(request.args.get('chat_number', type=int))

# /all_chats_for_user?user_name=NAME
# return list logins
@app.route('/all_chats_for_user')
def all_chats_for_user():
    return api.all_chats_for_user(request.args.get('user_name', type=str))

# /send_message?user_name=NAME&chat_number=1&message=MESSAGE
@app.route('/send_message')
def send_message():
    return api.send_message(request.args.get('user_name', type=str), request.args.get('chat_number', type=int), request.args.get('message', type=str))

# /get_messages?chat_number=1
# return list messages
@app.route('/get_messages')
def get_messages():
    return api.list_messages(request.args.get('chat_number', type=int))

# /get_messages_notifications?user_name=NAME
# return list notifications
@app.route('/get_messages_notifications')
def get_messages_notifications():
    return api.get_messages_notifications(request.args.get('user_name', type=str))

# /delete_message_notification?user_name=NAME&chat_number=1
@app.route('/delete_message_notification')
def delete_message_notification():
    return api.delete_message_notification(request.args.get('user_name', type=str), request.args.get('chat_number', type=int))

if __name__ == '__main__':
    app.run()

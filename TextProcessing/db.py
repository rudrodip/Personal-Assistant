import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred)

print('successfully initialized firebase')

db = firestore.client()
context_ref = db.collection('context')
chat_log_ref = context_ref.document('chat-log')
personal_data_ref = context_ref.document('personal-data')
bot_data_ref = context_ref.document('bot-data')
memory_ref = context_ref.document('memory')

# getters
def get_chat_log():
    data = chat_log_ref.get()
    data = data.to_dict()
    return data

def get_personal_data():
    data = personal_data_ref.get()
    data = data.to_dict()
    return data

def get_bot_data():
    data = bot_data_ref.get()
    data = data.to_dict()
    return data

def get_memory():
    data = memory_ref.get()
    data = data.to_dict()
    return data

def set_description(prev_desc, new_desc):
    new_desc = prev_desc + new_desc
    new_desc = {
        'description': new_desc
    }
    personal_data_ref.set(new_desc, merge=True)
    print('updated description')


# setters
def set_memory(field, data):
    ref = context_ref.document('memory')
    data = {
        field: data
    }
    ref.set(data, merge=True)
    print('updated memory')

def set_chat_log(prev_log, new_log):
    log = f'{prev_log}{new_log}'
    chat_log = {
        'conversation': log
    }

    chat_log_ref.set(chat_log, merge=True)
    print('updated chat-log')
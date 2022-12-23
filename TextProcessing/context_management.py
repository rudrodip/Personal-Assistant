from TextProcessing.db import *

def personal_context():
    context = get_personal_data()
    fullname, nickname, birthday, qualification = (
        context["fullname"],
        context["nickname"],
        context["birthday"],
        context["qualification"]
    )

    desc = context["description"]
    desc = desc.format(fullname=fullname, nickname=nickname, birthday=birthday, qualification=qualification)

    return desc

def chat_log():
    log = get_chat_log()['conversation']
    return log

def bot_data():
    data = get_bot_data()['name']
    return data

def memory_data():
    memory = get_memory()
    mems = ''
    for mem in memory:
        mems += f'{memory[mem]}\n'
    return mems

personal_context = personal_context()
bot_data = bot_data()
memory = memory_data()
chat_logs = chat_log()

def create_context(memory_refresh=False, chat_refresh=False):
    global personal_context
    global bot_data
    global memory
    global chat_logs

    if memory_refresh:
        memory = memory_data()

    if chat_refresh:
        chat_logs = chat_log()

    context = f'{personal_context}\n{memory}{chat_logs}'
    return context
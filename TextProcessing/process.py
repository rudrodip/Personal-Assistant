import openai
import os
import json
from TextProcessing import context_management

OPEN_AI_TOKEN = os.environ['OPENAI']
openai.api_key = OPEN_AI_TOKEN

class TextProcessor:
    def text_generator(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=300,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0,
        )
        try:
            answer = response.choices[0].text.strip()
        except:
            answer = None
        return answer


    def image_generator(self, prompt, n=1):
        response = openai.Image.create(prompt=prompt, n=n, size="512x512")
        image_urls = response["data"]
        for url in image_urls:
            yield url['url']

class Response(TextProcessor):
    max_length = 20
    chat_log = []
    context = context_management.create_context()

    def __init__(self, config_path):
        # getting the config file
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.author = self.config["author_name"]
        self.bot = self.config["bot_name"]

    def get_context(self):
        string = self.string_repr(self.chat_log)
        context = f'{self.context}\n{string}'
        
        return context
        
    def get_response(self, text, author=None, save=False):
        if text == "hi":
            return "Hi ! 💙 😊"

        context = self.get_context()

        if text == 'get-context':
            print(self.context)
            return 'debugged context'

        if text == 'get-context-full':
            print(context)
            return 'debugging full context'

        prompt = f"{context}\n{self.author} : {text}"
        response = self.text_generator(prompt)
        response = response.lstrip(f'{self.bot}:').strip()

        if author:
            self.set_chat_log(text, response, author, self.bot)
        else:
            self.set_chat_log(text, response, self.author, self.bot)

        if text.startswith('remember'):
            last_chat = [self.chat_log[-1]]
            context_management.set_chat_log(context_management.chat_logs, self.string_repr(last_chat))
            self.context = context_management.create_context(chat_refresh=True)

        if save and len(self.chat_log) >= self.max_length:
            context_management.set_chat_log(context_management.chat_logs, self.string_repr(self.chat_log))
            self.chat_log = []
            self.context = context_management.create_context(chat_refresh=True)

        return response

    # append chat log
    def set_chat_log(self, prompt, answer, author, bot):
        chat = {
            author: prompt,
            bot: answer
        }
        if len(self.chat_log) < self.max_length:
            self.chat_log.append(chat)
        else:
            self.chat_log.pop(0)
            self.chat_log.append(chat)

    # string representation of chat
    def string_repr(self, chat_logs):
        string = ''
        for chat in chat_logs:
            for key in chat:
                string += f'{key}: {chat[key]}\n'
        return string
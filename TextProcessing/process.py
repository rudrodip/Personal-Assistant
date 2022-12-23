import openai
import os
import json
import context_management

OPEN_AI_TOKEN = os.environ['OPENAI']
openai.api_key = OPEN_AI_TOKEN

class TextProcessor:
    def text_generator(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=500,
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
    max_length = 50
    chat_log = []
    context = context_management.create_context()

    def __init__(self, config_path):
        # getting the config file
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.author = self.config["author_name"]
        self.bot = self.config["bot_name"]

    def get_context(self):
        context = f'{self.context}\n'
        for chat in self.chat_log:
            ch = f'{self.author}: {chat[self.author]}\n{self.bot}: {chat[self.bot]}\n'
            context += ch
        
        return context
        
    def get_response(self, text, save=False):
        if text == "hi":
            return "Hi ! 💙 😊"

        context = self.get_context()

        if text == 'get-context':
            return self.context

        if text == 'get-context-full':
            return context

        prompt = f"{context}\n{self.author} : {text}"
        response = self.text_generator(prompt)
        response = response.lstrip(f'{self.bot}:').strip()

        self.set_chat_log(text, response, self.author, self.bot)

        if text.startswith('remember'):
            save = True

        if save and len(self.chat_log) >= self.max_length:
            context_management.set_chat_log(context_management.chat_logs, self.string_repr())
            self.chat_log = []
            self.context = context_management.create_context(chat_refresh=True)

        return response

    # append chat log
    def set_chat_log(self, prompt, answer, author, bot):
        chat = {
            author: prompt,
            bot: answer
        }
        if len(self.chat.log) < self.max_length:
            self.chat_log.append(chat)
        else:
            self.chat_log.pop(0)
            self.chat_log.append(chat)

    # string representation of chat
    def string_repr(self):
        string = ''
        for chat in self.chat.log:
            for key in chat:
                string += f'{key}: {chat[key]}\n'
        return string
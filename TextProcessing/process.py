import openai
import os
import json

OPEN_AI_TOKEN = os.environ['OPENAI']
openai.api_key = OPEN_AI_TOKEN

class TextProcessor:
    def text_generator(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=200,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0,
        )
        try:
            answer = response.choices[0].text.strip()
        except:
            answer = None
        return answer


    def image_generator(self, prompt):
        response = openai.Image.create(prompt=prompt, n=2, size="512x512")
        image_urls = response["data"]
        for url in image_urls:
            yield url['url']

class Response(TextProcessor):
    chat_log_path = "./TextProcessing/Database/chat_log.txt"
    def __init__(self, config_path):
        # getting the config file
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # getting previous chat log
        with open(self.chat_log_path, 'r', encoding="utf-8") as f:
            self.chat_log = f.read()

    def get_context(self):
        personal_context = self.config["personal_context"]
        chat_log = self.chat_log

        context = f'{personal_context}\n{chat_log}'
        return context

    def create_context(self, author, text, response):
        with open(self.chat_log_path, 'a', encoding="utf-8") as f:
            print('writing to context...')
            f.write(f"\n{author}: {text}\n{response}")
        
    def get_response(self, text):
        if text == "hi":
            return "Hi ! 💙 😊"

        author = self.config["author_name"]
        bot = self.config["bot_name"]

        context = self.get_context()
        print(context)
        prompt = f"{context}\n{author} : {text}"
        response = self.text_generator(prompt)

        self.create_context(author, text, response)

        response = response.replace(f'{bot}:', '').strip()
        return response
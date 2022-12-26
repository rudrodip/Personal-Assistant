import json

class TextProcessor:
    def text_generator(self, prompt):
        return prompt

    def image_generator(self):
        return 'babe.png'

class Response(TextProcessor):
    def __init__(self, config_path):
        # getting the config file
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.author = self.config["author_name"]
        self.bot = self.config["bot_name"]
        
    def get_response(self, text):
        return self.text_generator(text)
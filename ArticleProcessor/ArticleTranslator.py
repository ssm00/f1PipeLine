import openai
import json
import os


#v1은 단일 기사 번역

class ArticleTranslator:
    def __init__(self, prompt, key):
        self.prompt = prompt
        self.client = openai.OpenAI(api_key=key)

    def translate_v1(self, content):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": content}
            ]
        )
        return completion.choices[0].message.content


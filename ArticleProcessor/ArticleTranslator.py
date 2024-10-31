import openai
import json
import os
import anthropic
from util.commonException import CommonError, ErrorCode

#v1은 단일 기사 번역

class ArticleTranslator:
    def __init__(self, prompt_json, key_json):
        self.prompt_version = prompt_json.get("version")
        if self.prompt_version == "v1":
            self.prompt = prompt_json.get("prompt_v1")

        self.model = key_json.get("model")
        if self.model =="gpt":
            self.client = openai.OpenAI(api_key=key_json.get("open_ai_api_key"))
        elif self.model == "claude":
            self.client = anthropic.Anthropic(api_key=key_json.get("claude_api_key"))

    def translate_v1(self, content):
        try:
            if self.model == "gpt":
                completion = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.prompt},
                        {"role": "user", f"content": f"Please summarize and translate the following Formula One article according to the given instructions:\n\n{content}"}
                    ]
                )
                translate_content_json = completion.choices[0].message.content
            else:
                # 기본 self.client.messages.create
                # 캐시 사용 비용 40~50프로 절감 굳
                completion = self.client.beta.prompt_caching.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=2000,
                    temperature=0.0,
                    system=[
                        {
                            "type":"text",
                            "text":self.prompt,
                            "cache_control":{"type": "ephemeral"}
                        }],
                    messages=[
                        {"role": "user", "content": f"Please summarize and translate the following Formula One article according to the given instructions:\n\n{content}"}
                    ]
                )
                translate_content_json = completion.content[0].text
                return json.loads(translate_content_json)
        except json.decoder.JSONDecodeError as e:
            try:
                start_index = translate_content_json.find('{')
                processed_string = translate_content_json[start_index:]
                translate_content = json.loads(processed_string)
                return translate_content_json
            except json.decoder.JSONDecodeError as e:
                raise CommonError(ErrorCode.JSON_DECODE_ERROR, "잘못된 형식의 JSON 반환", translate_content_json, e)
        except anthropic.InternalServerError as err:
            if err.status_code == "529":
                raise CommonError(ErrorCode.SERVER_BUSY,"anthropic 서버 과부화 나중에 일단 넘어감 나중에 다시 시도", completion, e)


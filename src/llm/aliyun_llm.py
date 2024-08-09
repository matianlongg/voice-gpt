from http import HTTPStatus
from src.llm.base import LLM
from dashscope import Generation

class AliyunLLM(LLM):
    def __init__(self, api_key=None, model='qwen-turbo', **kwargs):
        import dashscope
        dashscope.api_key = api_key
        self.model = model
        self.prompt = ""  # 初始化时传入的prompt配置

    def __call__(self, text):
        messages = [{'role': 'user', 'content': text}]
        # 调用OpenAI的大模型API，并返回结果
        responses = Generation.call(
            model=self.model,
            messages=messages,
            result_format='message',  # set result format as 'message'
            stream=True,  # enable stream output
            incremental_output=True,  # enable incremental output
        )
        answer = ""
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                answer += response.output.choices[0]['message']['content']
            else:
                print(
                    'Request id: %s, Status code: %s, error code: %s, error message: %s'
                    % (
                        response.request_id,
                        response.status_code,
                        response.code,
                        response.message,
                    ))
        return answer
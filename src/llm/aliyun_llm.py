from http import HTTPStatus
from src.llm.base import LLM
from dashscope import Generation
from src.memory.base import Memory

class AliyunLLM(LLM):
    def __init__(self, api_key=None, model='qwen-turbo', memory: Memory=None, **kwargs):
        import dashscope
        dashscope.api_key = api_key
        self.model = model
        self.prompt = ""  # 初始化时传入的prompt配置
        self.message_history = [{"role": "system", "content": self.prompt}]
        self.memory = memory
        self.user_id = 1


    def __call__(self, text):
        prompt = text
        if self.memory:
            previous_memories = self.memory.search_memories(text, user_id=self.user_id)
            if previous_memories:
                prompt = f"用户输入: {text}\n 以前的记忆: {previous_memories}"
        self.message_history.append({"role": "user", "content": prompt})

        # 调用OpenAI的大模型API，并返回结果
        responses = Generation.call(
            model=self.model,
            messages=self.message_history,
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
        self.message_history.append({"role": "assistant", "content": answer})
        if self.memory:
            self.memory.add_memories(text, user_id=self.user_id)
        return answer
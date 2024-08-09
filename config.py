import os
import yaml
from dotenv import load_dotenv
from string import Template

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

def load_yaml_with_env(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        # 读取 YAML 文件内容
        yaml_content = file.read()
        # 使用 string.Template 来替换 ${} 中的值
        template = Template(yaml_content)
        # yaml_content_with_env = template.substitute(os.environ)
        yaml_content_with_env = template.safe_substitute({
            'DASHSCOPE_API_KEY': os.getenv('DASHSCOPE_API_KEY', 'EMPTY'),
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', 'EMPTY'),
            'OPENAI_BASE_URL': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        })
        # 将替换后的字符串加载为字典
        return yaml.safe_load(yaml_content_with_env)

# 加载 settings.yaml 文件
config = load_yaml_with_env('settings.yaml')
# 你可以在这里添加其他配置初始化逻辑


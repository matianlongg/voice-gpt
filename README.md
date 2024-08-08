# Voice-GPT

Voice-GPT 使用大语言模型实现语音交互的项目。

语音识别 -> 大语言模型 -> 语音输出

## 安装

### 1.克隆仓库

```bash
git clone https://github.com/matianlongg/voice-gpt.git
cd voice-gpt
```

### 2.安装依赖项

```bash
pip install -r requirements.txt
```

### 3.设置环境变量

在根目录根据 .env.template 创建 .env 文件，并添加您的 API 密钥和配置。例如：

```makefile
DASHSCOPE_API_KEY=sk-2*********
```

### 4.运行应用程序

```bash
python main.py
```

## 使用方法

### 1.启动应用程序

```bash
python main.py
```

### 2.使用语音命令进行互动

- 对着麦克风说话。
- 系统会识别您的语音，将其转换为文本，使用大语言模型处理查询，并提供语音响应。

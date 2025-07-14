# from langchain.chains import ConversationChain
# from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
#
# def get_chat_response(prompt,memory,openai_api_key):
#     '''
#     获取AI聊天响应的核心函数
#     :param prompt: 用于输入的问题或提示
#     :param memory: 对话内存对象，存储历史对话
#     :param openai_api_key: OpenAI API密钥
#     :return: AI生成的回答文本
#     '''
#     model = ChatOpenAI(
#         model='gpt-3.5-turbo',
#         openai_api_key=openai_api_key,
#         openai_api_base='https://api.openai-hk.com/v1/'
#     )
#
#     chain = ConversationChain(llm=model,memory=memory)
#     response = chain.invoke({'input':prompt})
#     return response['response']


from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import json
from datetime import datetime


def get_chat_response(prompt, memory, openai_api_key, model_name='gpt-3.5-turbo', temperature=0.7, max_tokens=500):
    '''
    获取AI聊天响应的核心函数
    :param prompt: 用于输入的问题或提示
    :param memory: 对话内存对象，存储历史对话
    :param openai_api_key: OpenAI API密钥
    :param model_name: 模型名称
    :param temperature: 创造力参数
    :param max_tokens: 最大回复长度
    :return: AI生成的回答文本
    '''
    model = ChatOpenAI(
        model=model_name,
        openai_api_key=openai_api_key,
        openai_api_base='https://api.openai-hk.com/v1/',
        temperature=temperature,
        max_tokens=max_tokens
    )

    chain = ConversationChain(llm=model, memory=memory)
    response = chain.invoke({'input': prompt})
    return response['response']


def export_conversation(messages, filename=None):
    '''
    导出对话记录功能
    :param messages: 对话消息列表
    :param filename: 文件名（可选）
    :return: 导出的文件内容
    '''
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"

    # 准备导出数据
    export_data = {
        "export_time": datetime.now().isoformat(),
        "total_messages": len(messages),
        "conversation": messages
    }

    # 转换为JSON字符串
    json_content = json.dumps(export_data, ensure_ascii=False, indent=2)

    return json_content, filename


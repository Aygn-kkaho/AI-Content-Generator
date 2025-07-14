from prompt_template import system_template_text, user_template_text
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from xiaohongshu_model import Xiaohongshu

def generate_xiaohongshu(theme, openai_api_key, style):
    prompt = ChatPromptTemplate.from_messages([
        ('system', system_template_text),
        ('user', user_template_text)
    ])
    model = ChatOpenAI(
        model='gpt-3.5-turbo',
        base_url='https://api.openai-hk.com/v1/',
        openai_api_key=openai_api_key
    )

    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)

    chain = prompt | model | output_parser

    result = chain.invoke({
        'theme': theme,
        'style': style,
        'parser_instructions': output_parser.get_format_instructions()
    })
    return result
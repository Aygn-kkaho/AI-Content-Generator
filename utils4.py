from langchain.chains import ConversationalRetrievalChain
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from prompt_template import ai_style_instructions


def qa_agent(openai_api_key, memory, uploaded_file, question, temperature=0.3, max_tokens=500, ai_style="正式性"):
    '''
    PDF智能问答代理核心函数
    :param openai_api_key: OpenAI API密钥
    :param memory: 对话内存，存储历史对话
    :param uploaded_file: 上传的PDF文件对象
    :param question: 用户提出的问题
    :param ai_style: 用户选择的AI回答风格
    :return: AI基于PDF内容生成的回答
    '''

    model = ChatOpenAI(
        model='gpt-3.5-turbo',
        openai_api_key=openai_api_key,
        openai_api_base='https://api.openai-hk.com/v1/',
        temperature=temperature,
        max_tokens=max_tokens
    )

    #读取上传的PDF文件内容
    file_content = uploaded_file.read()


    #临时保存上传的PDF文件到本地
    #由于LangChain的PDFLoader需要文件路径，所以需要先保存文件
    # temp_file_path = 'temp.pdf'
    # with open(temp_file_path,'wb') as temp_file:
    #     temp_file.write(file_content)

    temp_file_path = 'temp'
    with open(temp_file_path,'wb') as temp_file:
        temp_file.write(file_content)


    loder = PyPDFLoader(temp_file_path)


    docs = loder.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 每个文本块的最大长度
        chunk_overlap=50,  # 相邻文本块之间的重叠字符数
        separators=['\n\n', '\n', '。', '!', '?', '，', '、', '']  # 定义文本的分隔符，按照优先级从高到低排列
    )

    texts = text_splitter.split_documents(docs)

    embeddings_model=OpenAIEmbeddings(
        model='text-embedding-3-large',
        openai_api_key='hk-od7yyv100005693148ffff26a3d09e5ac33ad5d554bbccb8',
        openai_api_base='https://api.openai-hk.com/v1/'
    )
    # 使用FAISS向量存储库，将分割后的文本块和嵌入模型结合
    db = FAISS.from_documents(texts, embeddings_model)

    # 将向量存储转换为检索器，用于后续查询
    retriever = db.as_retriever()

    # 拼接风格指令到用户问题
    style_prompt = f"请用如下风格回答问题：{ai_style}\n{ai_style_instructions}\n问题：{question}"

    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
    )

    def convert_memory_to_list(memory_obj):
        history_list = []
        messages = memory_obj.chat_memory.messages
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                human = messages[i].content
                ai = messages[i + 1].content
                history_list.append((human, ai))
        return history_list

    chat_history = convert_memory_to_list(memory)

    # response = qa.invoke({'chat_history':chat_history,'question':style_prompt})
    response = qa.invoke({'question': style_prompt})

    return response





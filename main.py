import os
from datetime import datetime

import streamlit as st
from utils1 import generate_script, download_script_as_excel
from utils2 import generate_xiaohongshu
from utils3 import get_chat_response, export_conversation
from utils4 import qa_agent
from langchain.memory import ConversationBufferMemory
from get_image import get_images_from_baidu
# 设置页面配置
st.set_page_config(
    page_title="🌐 AI多功能内容生成器",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1lcbmhc {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div > label {
        color: white !important;
    }
    
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .content-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #d1d8e0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .result-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .result-title {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .result-content {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .sidebar-container {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
        border: 1px solid #5a6fd8;
    }
    
    .sidebar-container h3 {
        color: white;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .stSelectbox > div > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stSelectbox > div > div > div > div {
        background: rgba(255, 255, 255, 0.9);
    }
    
    .info-box {
        background: linear-gradient(45deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .success-box {
        background: linear-gradient(45deg, #00b894, #00a085);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    .chat-message {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .chat-message.user {
        background: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .chat-message.ai {
        background: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .file-upload-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        border: 2px dashed #667eea;
        margin-bottom: 1rem;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        margin-top: 1rem;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    .st-emotion-cache-1h9usn1.eah1tn13 {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: 1rem;
        border: 1px solid #e0e0e0;  
    }

    
</style>
""", unsafe_allow_html=True)

# 主标题区域
st.markdown("""
<div class="main-header">
    <h1>🌐 AI多功能内容生成器</h1>
    <p>一站式AI创作平台，让创意无限可能</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏配置
with st.sidebar:

    st.markdown("""
    <div class="sidebar-container">
        <h3>🔐 API 配置</h3>
    </div>
    """, unsafe_allow_html=True)

    openai_api_key = st.text_input(
        '🗝️ OpenAI API 密钥',
        type='password',
        placeholder='请输入你的 OpenAI API 密钥'
    )

    st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <a href="https://openai-hk.com/v3/ai/key" target="_blank" 
           style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); 
                  padding: 0.5rem 1rem; border-radius: 20px; display: inline-block;">
           🔑 获取 API 密钥
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 功能说明
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: white; margin-bottom: 0.5rem;">🚀 功能特色</h4>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin: 0;">
        • 🎬 视频脚本生成<br>
        • 📱 小红书文案创作<br>
        • 💬 智能对话助手<br>
        • 📄 PDF文档问答
        </p>
    </div>
    """, unsafe_allow_html=True)

# 功能选择
selected_function = st.selectbox(
    '🎯 选择功能',
    ['视频脚本生成器', '小红书文案生成器', '克隆GPT对话', 'PDF问答工具'],
    help='选择你想要使用的AI功能'
)

# =================视频脚本===========
if selected_function == '视频脚本生成器':

    if 'memory_video' not in st.session_state:
        st.session_state['memory_video'] = ConversationBufferMemory(return_messages=True)
        st.session_state['messages_video'] = [{'timestamp':datetime.now(),
                                         'role': 'ai',
                                         '主题': 'subject',
                                         'title':'⌚ Begin',
                                         'content': '你好，我是视频脚本生成器，有什么可以帮助你的吗？'}]


    subject = st.text_input(
        '💡 视频主题',
        placeholder='例如：如何提高工作效率、美食制作教程、旅行攻略等',
        help='请输入你想要制作视频的主题'
    )

    col1, col2 = st.columns(2)
    with col1:
        video_length = st.number_input(
            '⏱️ 视频时长（分钟）',
            min_value=0.5,
            max_value=60.0,
            value=3.0,
            step=0.5,
            help='设置视频的大致时长'
        )

    with col2:
        creativity = st.slider(
            '⭐ 创造力参数',
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.1,
            help='数值越小越严谨，数值越大越有创意'
        )

    col1, col3 = st.columns(2)  # 最右边是窄列

    with col1:
        submit = st.button('🚀 生成视频脚本', use_container_width=True)

    with col3:
        if 'messages_video' in st.session_state:
            buffer = download_script_as_excel(messages=st.session_state['messages_video'] )
            st.download_button(
                label="📥 下载脚本为Excel",
                data=buffer,
                file_name="script.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )


    if submit and not subject:
        st.markdown('<div class="info-box">⚠️ 请输入视频主题</div>', unsafe_allow_html=True)
        st.stop()


    if submit:
        with st.spinner(''):
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <div style="font-size: 1.2rem; color: #667eea; font-weight: bold;">AI 正在思考中，请稍候...</div>
            </div>
            """, unsafe_allow_html=True)

            try:
                title, respond_script = generate_script(subject, video_length, creativity, openai_api_key)

                st.markdown('<div class="success-box">✅ 视频脚本生成成功！</div>', unsafe_allow_html=True)

                st.markdown("""
                <div class="result-container">
                    <div class="result-title">🔥 视频标题</div>
                    <div class="result-content">{}</div>
                </div>
                """.format(title), unsafe_allow_html=True)

                st.markdown("""
                <div class="result-container">
                    <div class="result-title">📚 完整脚本</div>
                    <div class="result-content">{}</div>
                </div>
                """.format(respond_script.replace('\n', '<br>')), unsafe_allow_html=True)

                msg = {'timestamp': datetime.now(),
                       'role': 'ai',
                       '主题': subject,
                       'title': '🔥' + title,
                       'content': respond_script,
                       }
                st.session_state['messages_video'].append(msg)

                # for message in st.session_state['messages_video']:
                #     # st.chat_message(message['role']).write(message['content'])
                #     expander = st.expander(message['title'])
                #     expander.write(message['content'])
                #     # expander.image("https://static.streamlit.io/examples/dice.jpg")

                st.markdown("""
                    <style>
                    summary {
                        font-size: 1.5rem !important;
                        font-weight: bold !important;
                        color: white !important;
                        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
                    }
                    </style>
                """, unsafe_allow_html=True)

                for message in st.session_state['messages_video']:
                    with st.expander(message['title']):
                        st.markdown(f"""
                        <div class="result-content">
                            {message['content']}
                        </div>
                        """, unsafe_allow_html=True)

                # for i, message in enumerate(st.session_state['messages_video']):
                #     # 给每个expander一个唯一ID以便CSS样式生效（可选）
                #     st.markdown(f"""
                #     <style>
                #         div[data-testid="stExpander"][id="expander-{i}"] {{
                #             background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                #             border-radius: 15px;
                #             padding: 10px;
                #             box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                #             margin-bottom: 1rem;
                #             border: 1px solid #e0e0e0;
                #         }}
                #     </style>
                #     """, unsafe_allow_html=True)
                #
                #     # 插入内容
                #     with st.expander(message['title']):
                #         st.markdown(f"""
                #         <div class="result-content">
                #             {message['content']}
                #         </div>
                #         """, unsafe_allow_html=True)


            except Exception as e:
                st.error(f"❌ 生成失败：{str(e)}")
                st.info("请检查你的 API 密钥是否正确，或者稍后重试")

    st.markdown("</div>", unsafe_allow_html=True)



# ========== 小红书文案 ===========
elif selected_function == '小红书文案生成器':

    theme = st.text_input(
        '🎯 文案主题',
        placeholder='例如：护肤心得、美食分享、旅行攻略、穿搭推荐等',
        help='请输入你想要生成的小红书文案主题'
    )

    styles = ["幽默", "文艺", "专业", "严肃"]
    selected_style = st.selectbox("🎯 选择写作风格", styles)

    submit = st.button('✍️ 开始写作', use_container_width=True)

    if submit and not openai_api_key:
        st.info('请输入你的0penAI API密钥')
        st.stop()

    if submit and not theme:
        st.info('请输入小红书文案的主题')
        st.stop()

    if __name__ == "__main__":
        keyword = theme
        page_num = 5
        page_num = int(page_num)
        save_dir = '.\\百度图片\\' + keyword
        get_images_from_baidu(keyword, page_num, save_dir)

    if submit:
        with st.spinner('🤖 ai正在思考中，请稍后...'):
            result = generate_xiaohongshu(theme, openai_api_key,selected_style)
        st.divider()


        st.markdown('<div class="success-box">🎉小红书文案生成成功！</div>', unsafe_allow_html=True)

        left_column, right_column = st.columns(2)

        with left_column:
            st.markdown("""
            <div class="result-container">
                <div class="result-title">📝 推荐标题</div>
            </div>
            """, unsafe_allow_html=True)

            for i, title in enumerate(result.title, 1):
                st.markdown(f"### 标题 {i}：")
                st.markdown(f"<div class='result-content'>{title}</div>", unsafe_allow_html=True)
                st.markdown("---")

            with st.expander('相关图片'):
                image_files = [os.path.join(save_dir, f) for f in os.listdir(save_dir) if
                               f.endswith('.jpg') and 1 <= int(f.split('.')[0]) <= 5]
                for image_path in image_files:
                    st.image(image_path, caption=image_path.split('/')[-1], use_container_width=True)


        with right_column:
            # st.markdown('##### 小红书正文')
            st.markdown("""
                          <div class="result-container">
                              <div class="result-title">📖 正文内容</div>
                              <div class="result-content">{}</div>
                          </div>
                          """.format(result.content.replace('\n', '<br>')), unsafe_allow_html=True)




#  =========== 克隆GPT==========
elif selected_function == '克隆GPT对话':


    # 新增：对话管理
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('新建对话'):
            st.session_state['messages'] = []
            st.session_state['memory'] = ConversationBufferMemory(return_messages=True)
    with col2:
        if st.button('清空历史'):
            st.session_state['messages'] = []
    with col3:
        if st.button('导出对话'):
            if 'messages' in st.session_state and st.session_state['messages']:
                json_content, filename = export_conversation(st.session_state['messages'])
                st.download_button(
                    label="下载对话记录",
                    data=json_content,
                    file_name=filename,
                    mime="application/json"
                )

    # 新增：参数调节
    temperature = st.slider('创造力', 0.0, 1.0, 0.7)
    max_tokens = st.number_input('最大回复长度', 100, 2000, 500)
    if 'memory' not in st.session_state:
        st.session_state['memory'] = ConversationBufferMemory(return_messages=True)
        st.session_state['messages'] = [{'role': 'ai', 'content': '你好，我是你的AI助手，有什么可以帮你的吗？'}]


    # 显示历史对话消息
    st.markdown("""
    <div class="chat-container">
        <div class="result-title">💬 对话历史</div>
    </div>
    """, unsafe_allow_html=True)

    for message in st.session_state['messages']:
        role_class = 'user' if message['role'] == 'human' else 'ai'
        st.markdown(f"""
        <div class="chat-message {role_class}">
            <strong>{'👤 用户' if message['role'] == 'human' else '🤖 AI助手'}:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)

    prompt = st.chat_input("💭 输入你的问题...")

    if prompt:
        if not openai_api_key:
            st.markdown('<div class="info-box">⚠️ 请输入你的 OpenAI API 密钥</div>', unsafe_allow_html=True)
            st.stop()

        # 添加用户消息到对话历史
        st.session_state['messages'].append({'role': 'human', 'content': prompt})

        with st.spinner(''):
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                <div style="font-size: 1rem; color: #667eea; font-weight: bold;">AI 正在思考中，请稍候...</div>
            </div>
            """, unsafe_allow_html=True)

            try:
                response = get_chat_response(prompt, st.session_state['memory'], openai_api_key)

                msg = {'role': 'ai', 'content': response}
                st.session_state['messages'].append(msg)

                st.rerun()

            except Exception as e:
                st.error(f"❌ 对话失败：{str(e)}")
                st.info("请检查你的 API 密钥是否正确，或者稍后重试")

    st.markdown("</div>", unsafe_allow_html=True)



# ========PDF问答工具=============
elif selected_function == 'PDF问答工具':

    if 'memory' not in st.session_state:
        st.session_state['memory'] = ConversationBufferMemory(
            return_messages=True,
            memory_key='chat_history',
            output_key='answer'
        )

    uploaded_file = st.file_uploader('📁 上传PDF文件(最大文件大小100MB)', type='pdf')

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider('💡 创造力', 0.0, 1.0, 0.3, step=0.05, help='数值越大，回答更有创意')
    with col2:
        max_tokens = st.number_input('📃 最大回复长度', 100, 2000, 500, step=100, help='限制AI回答的最大字数')

    # 新增：AI回答风格选择
    style_options = ["正式性", "非正式性", "技术性", "简洁直接性", "解释性"]
    ai_style = st.selectbox('🤖 选择AI回答风格', style_options, index=0, help='选择AI生成答案的风格')

    question = st.text_input(
        '❓ 对PDF内容进行提问',
        placeholder='例如：文档的主要内容是什么？请总结一下...',
        disabled=not uploaded_file,
        help='输入你想要询问的问题'
    )

    if uploaded_file and question and not openai_api_key:
        st.markdown('<div class="info-box">⚠️ 请输入你的 OpenAI API 密钥</div>', unsafe_allow_html=True)
        st.stop()

    if uploaded_file and question and openai_api_key:
        with st.spinner('🤖 ai正在思考中，请稍后...'):
            response = qa_agent(
                openai_api_key,
                st.session_state['memory'],
                uploaded_file,
                question,
                temperature=temperature,
                max_tokens=max_tokens,
                ai_style=ai_style
            )
        st.divider()

        st.markdown("""
        <div class="result-container">
            <div class="result-title">💡 AI 答案</div>
            <div class="result-content">{}</div>
        </div>
        """.format(response['answer'].replace('\n', '<br>')), unsafe_allow_html=True)

        st.session_state['chat_history'] = response['chat_history']


    if 'chat_history' in st.session_state:
        st.divider()
        with st.expander('📚 历史对话记录'):
            for i in range(0, len(st.session_state['chat_history']), 2):
                if i + 1 < len(st.session_state['chat_history']):
                    human_message = st.session_state['chat_history'][i]
                    ai_message = st.session_state['chat_history'][i + 1]

                    st.markdown("**👤 问题：**")
                    st.write(human_message.content)
                    st.markdown("**🤖 答案：**")
                    st.write(ai_message.content)

                    if i < len(st.session_state['chat_history']) - 2:
                        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)


# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 2rem 0;">
    <p>🌐 AI多功能内容生成器 | 让创作更简单</p>
    <p style="font-size: 0.9rem;">Powered by OpenAI & Streamlit</p>
</div>
""", unsafe_allow_html=True)
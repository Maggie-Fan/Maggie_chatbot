import streamlit as st

st.set_page_config(
    page_title="Maggie Chatbot Hub",
    page_icon="🧠",
    layout="wide"
)

st.title("🤖 Maggie 多功能聊天助理")
st.markdown("""
### 🎉 歡迎來到 Maggie 的聊天機器人總覽！
請從左側 Sidebar 選擇以下功能頁面：

- 🗞️ 新聞聊天機器人：回答與新聞相關的問題
- 📍 Word2Vec 2D：視覺化詞嵌入的 2D 效果
- 🧊 Word2Vec 3D：視覺化詞嵌入的 3D 模型
- 💡 Skip-Gram：Skip-gram 模型查詢詞彙
- 🔤 CBOW：CBOW 模型查詢詞彙

👉 選擇任一功能後，可使用 chat_input 與模型互動
""")


#import streamlit as st

#st.set_page_config(page_title="Maggie's Chatbot ", layout="wide")
#st.title("👋 Welcome to Maggie's Chatbot")
#st.write("請從左側選擇你要執行的功能頁面～")

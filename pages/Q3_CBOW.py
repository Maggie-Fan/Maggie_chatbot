# Q3_CBOW.py

import streamlit as st
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import remove_stopwords

st.set_page_config(page_title="Q3 CBOW ", layout="wide")
st.title("🔤 Q3: CBOW Word2Vec ")

# === 參數設定 ===
vector_size = 100
window_size = 5
min_count = 1
workers = 4

# === 語料來源 ===
sentences = [
    "Fifteen people in South Korea were injured, two of them seriously, after a pair of fighter jets accidentally dropped eight bombs in a civilian district on Thursday during a live-fire military exercise, local media reported",
    "The incident involving the Air Force KF-16 aircraft, in the city of Pocheon near North Korea, was part of routine drills held by the South to maintain combat readiness against potential attacks from the North",
    "South Korea's Air Force said that it was investigating the incident and apologised for the damage, adding it would provide compensation to those affected",
    "While shells from live firing exercises sometimes land near civilian residences, they rarely cause injuries",
    "According to local media reports, two people suffered fractures to their necks and shoulders",
    "The military said the pilot of one of the jets inputted the wrong coordinates by mistake, causing the bombs to drop in the civilian community",
    "Investigators have yet to determine why the second jet dropped its bombs, the military said, adding all live-fire exercises will be suspended",
    "One church building and houses were also damaged as a result of the incident",
    "South Korea and the US are set to run combined drills from March 10 to March 20 - the first since US president Donald Trump's return to the White House",
    "This comes at a time when the two countries are increasingly wary of the growing alliance between North Korea and Russia",
]

# === 預處理語料 ===
tokenized = [simple_preprocess(remove_stopwords(sentence)) for sentence in sentences]

# === 使用 cache 訓練 CBOW 模型 ===
@st.cache_resource
def train_cbow_model(tokenized_sentences):
    model = Word2Vec(tokenized_sentences, vector_size=vector_size, window=window_size, min_count=min_count, workers=workers, sg=0)
    return model

cbow_model = train_cbow_model(tokenized)

# === 顯示詞彙表 ===
with st.expander("📖 查看 CBOW 詞彙表"):
    st.write(cbow_model.wv.index_to_key)

# === 查詢相似詞區塊 ===
user_input = st.text_input("🔎 輸入一個詞，我會顯示 CBOW 的相似詞", key="cbow_query")

if user_input:
    st.write(f"你輸入的詞： `{user_input}`")
    if user_input in cbow_model.wv:
        similar = cbow_model.wv.most_similar(user_input, topn=5)
        st.markdown("**CBOW 模型 Top 5 相似詞：**\n" + "\n".join([f"- {w} ({sim:.2f})" for w, sim in similar]))
    else:
        st.warning("❌ 詞彙不在模型中，請嘗試其他詞。")
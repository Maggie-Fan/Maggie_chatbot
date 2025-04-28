# Q2_SkipGram.py

import streamlit as st
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import remove_stopwords

# 頁面設定
st.set_page_config(page_title="Q2 Skip-Gram Word2Vec", layout="wide")
st.title("📘 Q2: Word2Vec - Skip-Gram")

# === 模型參數設定 ===
vector_size = 100
window_size = 5
min_count = 1
workers = 4
sg_flag = 1

# === 輸入語料 ===
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

# === 停用詞選項 ===
use_stopwords = st.toggle("🧹 Remove stopwords before training", value=True)

# === 預處理函數＋模型訓練，使用 cache 儲存 ===
@st.cache_resource
def train_skipgram_model(sentences, remove_sw):
    if remove_sw:
        tokenized = [simple_preprocess(remove_stopwords(sentence)) for sentence in sentences]
    else:
        tokenized = [simple_preprocess(sentence) for sentence in sentences]
    model = Word2Vec(tokenized, vector_size=vector_size, window=window_size, min_count=min_count, workers=workers, sg=sg_flag)
    return model

model = train_skipgram_model(sentences, use_stopwords)

# === 說明狀態 ===
if use_stopwords:
    st.caption("🔍 Training with sentences **without stopwords**.")
else:
    st.caption("📄 Training with **full sentences**.")

# === 展示詞彙表 ===
with st.expander("📘 Show Vocabulary List"):
    st.write(model.wv.index_to_key)

# === 查詢區塊，改用 text_input 避免跳轉 ===
user_input = st.text_input("🔎 輸入一個詞，列出相似詞（使用 Skip-gram）", key="skipgram_query")

if user_input:
    st.write(f"你輸入的詞： `{user_input}`")
    if user_input in model.wv:
        similar = model.wv.most_similar(user_input, topn=5)
        st.markdown(
            f"**Top 5 相似詞 for `{user_input}`:**\n" + "\n".join([f"- {w} ({sim:.2f})" for w, sim in similar])
        )
    else:
        st.warning("❌ 這個詞不在語料庫中，請嘗試其他詞彙。")

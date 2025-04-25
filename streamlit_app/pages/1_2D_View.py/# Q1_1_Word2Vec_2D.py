# Q1_1_Word2Vec_2D.py

import streamlit as st
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import numpy as np

# === 頁面設定 ===
st.set_page_config(page_title="Q1-1 Word2Vec 2D View", layout="wide")
st.title("📍 Word2Vec - 2D Visualization")

# === 資料準備 ===
sentences = [
    "Fifteen people in South Korea were injured, two of them seriously, after a pair of fighter jets accidentally dropped eight bombs in a civilian district on Thursday during a live-fire military exercise, local media reported",
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

tokenized_sentences = [simple_preprocess(s) for s in sentences]
model = Word2Vec(tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)

# === 降維處理 ===
word_vectors = np.array([model.wv[word] for word in model.wv.index_to_key])
pca = PCA(n_components=2)
reduced_vectors = pca.fit_transform(word_vectors)

# === 顏色設定 ===
color_map = {i: c for i, c in enumerate(['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'pink', 'yellow', 'brown'])}
word_colors = []
for word in model.wv.index_to_key:
    for i, sentence in enumerate(tokenized_sentences):
        if word in sentence:
            word_colors.append(color_map[i])
            break


# === 畫圖主體 ===
scatter = go.Scatter(
    x=reduced_vectors[:, 0],
    y=reduced_vectors[:, 1],
    mode='markers+text',
    text=model.wv.index_to_key,
    textposition='top center',
    marker=dict(color=word_colors, size=10),
)


# === 加線條 ===
line_traces = []
for i, sentence in enumerate(tokenized_sentences):
    vecs = [reduced_vectors[model.wv.key_to_index[word]] for word in sentence if word in model.wv]
    if vecs:
        line_trace = go.Scatter(
            x=[v[0] for v in vecs],
            y=[v[1] for v in vecs],
            mode='lines',
            line=dict(color=color_map[i], width=1),
            name=f"Sentence {i+1}"
        )
        line_traces.append(line_trace)

# === 畫圖 ===
fig = go.Figure(data=[scatter] + line_traces)
fig.update_layout(title="2D Visualization of Word Embeddings", width=900, height=700)
st.plotly_chart(fig)



# === chat_input ===
if word := st.chat_input("🔎 輸入一個詞，我會找出相關詞"):
    st.chat_message("user").write(word)
    if word in model.wv:
        similar = model.wv.most_similar(word, topn=5)
        st.chat_message("assistant").markdown("Top 5 相似詞：\n" + "\n".join([f"- {w} ({sim:.2f})" for w, sim in similar]))
    else:
        st.chat_message("assistant").write("這個詞不在語料庫中。")

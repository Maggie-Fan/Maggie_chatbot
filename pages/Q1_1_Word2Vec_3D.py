# Q1_1_Word2Vec_3D.py

import streamlit as st
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import numpy as np

st.set_page_config(page_title="Q1-1 Word2Vec 3D View", layout="wide")
st.title("🧊 Word2Vec - 3D Visualization")

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

# === 使用 cache 儲存模型與降維結果 ===
@st.cache_resource
def get_model_and_vectors(tokenized_sentences):
    model = Word2Vec(tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)
    word_vectors = np.array([model.wv[word] for word in model.wv.index_to_key])
    pca = PCA(n_components=3)
    reduced_vectors = pca.fit_transform(word_vectors)
    return model, reduced_vectors

model, reduced_vectors = get_model_and_vectors(tokenized_sentences)

# === 顏色設定 ===
color_map = {i: c for i, c in enumerate(['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'pink', 'yellow', 'brown'])}
word_colors = []
for word in model.wv.index_to_key:
    for i, sentence in enumerate(tokenized_sentences):
        if word in sentence:
            word_colors.append(color_map[i])
            break

# === 繪圖區塊 ===
with st.container():
    scatter = go.Scatter3d(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        z=reduced_vectors[:, 2],
        mode='markers+text',
        text=model.wv.index_to_key,
        textposition='top center',
        marker=dict(color=word_colors, size=4),
        hovertemplate="Word: %{text}<br>Color: %{marker.color}"
    )

    # 只顯示部分句子的連線
    display_array = [False, True, False, False, True, False, False, False, False, True]

    line_traces = []
    for i, sentence in enumerate(tokenized_sentences):
        if display_array[i]:
            vecs = [reduced_vectors[model.wv.key_to_index[word]] for word in sentence if word in model.wv]
            if vecs:
                line_trace = go.Scatter3d(
                    x=[v[0] for v in vecs],
                    y=[v[1] for v in vecs],
                    z=[v[2] for v in vecs],
                    mode='lines',
                    line=dict(color=color_map[i], width=2),
                    showlegend=False
                )
                line_traces.append(line_trace)

    fig = go.Figure(data=[scatter] + line_traces)
    fig.update_layout(
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        title="3D Visualization of Word Embeddings",
        width=1000,
        height=800
    )
    st.plotly_chart(fig)

# === 查詢輸入區 ===
user_input = st.text_input("🔎 輸入一個詞，我會找出相關詞 (3D View)", key="word_query_3d")

if user_input:
    st.write(f"你輸入的詞： {user_input}")
    if user_input in model.wv:
        similar = model.wv.most_similar(user_input, topn=5)
        st.markdown("Top 5 相似詞：\n" + "\n".join([f"- {w} ({sim:.2f})" for w, sim in similar]))
    else:
        st.write("❌ 這個詞不在語料庫中。")

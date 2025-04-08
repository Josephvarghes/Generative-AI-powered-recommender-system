# streamlit_app.py

import streamlit as st
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load assessments
with open("data/assessments.json", "r") as f:
    assessments = json.load(f)

# Prepare embeddings (load only once)
if "embedding" not in assessments[0]:
    texts = [f"{a['name']} - {', '.join(a.get('test_types', []))}" for a in assessments]
    embeddings = model.encode(texts, show_progress_bar=True)
    for i, embed in enumerate(embeddings):
        assessments[i]["embedding"] = embed.tolist()

# Search function
def search(query, top_k=5):
    query_embedding = model.encode([query])
    all_embeddings = np.array([a["embedding"] for a in assessments])
    similarities = cosine_similarity(query_embedding, all_embeddings)[0]
    top_indices = similarities.argsort()[::-1][:top_k]
    results = []
    for idx in top_indices:
        a = assessments[idx]
        a["score"] = round(similarities[idx], 3)
        results.append(a)
    return results

# Streamlit UI
st.set_page_config(page_title="SHL Assessment Recommender", page_icon="🧠")
st.title("🧠 SHL Assessment Recommender")
st.markdown("Provide a job title or job description to find the best assessment match 🔍")

# Sample tips
with st.expander("💡 Input Tips (Click to expand)"):
    st.write("""
    - ✅ Be clear and concise: _"Retail cashier who manages money and helps customers."_
    - ✅ Use job responsibilities or soft skills too.
    - ❌ Avoid general terms like _"Test"_ or _"Employee"_.
    """)

# User input
query = st.text_area("✍️ Enter Job Role or Description:", height=100)

if st.button("🔍 Recommend Assessments"):
    if query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        results = search(query)
        st.success(f"🎯 Top {len(results)} Assessment Matches for your query")

        for res in results:
            st.markdown("---")
            st.markdown(f"### 📌 {res['name']} (Score: {res['score']})")
            st.markdown(f"**Test Types:** {', '.join(res['test_types'])}")
            st.markdown(f"**Duration:** {res['duration']}")
            st.markdown(f"**Remote Testing:** {res['remote_testing']} | **Adaptive:** {res['adaptive_support']}")
            st.markdown(f"[🔗 View on SHL]({res['url']})")

# Footer
st.markdown("---")
st.caption("🚀 Built by Joseph Varghese | AI Recommender System Project")

# semantic_search.py

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Step 1: Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ Step 2: Load the assessment data
with open("data/assessments.json", "r") as f:
    assessments = json.load(f)

# ✅ Step 3: Prepare embeddings for each assessment
def prepare_embeddings(assessments):
    texts = []
    for item in assessments:
        # Use both name + test types to improve embedding quality
        test_types = ", ".join(item.get("test_types", []))
        full_text = f"{item['name']} - {test_types}"
        texts.append(full_text)
    
    # Embed all assessment texts
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Save embeddings back into the assessments
    for i, embed in enumerate(embeddings):
        assessments[i]["embedding"] = embed.tolist()

    return assessments

# ✅ Step 4: Search function using cosine similarity
def search_assessments(query, assessments, top_k=5):
    query_embedding = model.encode([query])
    all_embeddings = np.array([a["embedding"] for a in assessments])
    similarities = cosine_similarity(query_embedding, all_embeddings)[0]
    
    # Get top matches
    top_indices = similarities.argsort()[::-1][:top_k]
    results = []
    for idx in top_indices:
        a = assessments[idx]
        a["score"] = round(similarities[idx], 3)
        results.append(a)
    return results

# ✅ Step 5: Run the full pipeline
if __name__ == "__main__":
    assessments = prepare_embeddings(assessments)

    query = input("🔍 Enter your job role or JD snippet: ")
    top_matches = search_assessments(query, assessments)

    print("\n🎯 Top Assessment Matches:\n")
    for match in top_matches:
        print(f"📌 {match['name']} (score: {match['score']})")
        print(f"🔗 {match['url']}")
        print(f"⏱️ {match['duration']} | Remote: {match['remote_testing']} | Adaptive: {match['adaptive_support']}")
        print(f"🧪 Types: {', '.join(match.get('test_types', []))}")
        print("-" * 60)

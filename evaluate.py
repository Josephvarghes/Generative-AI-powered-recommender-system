

from embedder import prepare_embeddings, search_assessments
import json

def recall_at_k(results, ground_truth, k):
    predicted = [item['name'] for item in results[:k]]
    return 1 if ground_truth in predicted else 0

def average_precision_at_k(results, ground_truths, k):
    score = 0.0
    hits = 0
    for i in range(k):
        if results[i]['name'] in ground_truths:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(ground_truths), k)

def evaluate_all(assessments, test_queries, k=5):
    print("🔧 Embedding all assessments...")
    assessments = prepare_embeddings(assessments)

    total_recall = 0
    total_ap = 0

    for item in test_queries:
        print(f"\n🔍 Query: {item['query']}")
        results = search_assessments(item['query'], assessments, top_k=k)

        r_at_k = recall_at_k(results, item['ground_truth'], k)
        ap_at_k = average_precision_at_k(results, [item['ground_truth']], k)

        total_recall += r_at_k
        total_ap += ap_at_k

        print(f"✅ Ground Truth: {item['ground_truth']}")
        print(f"📊 Recall@{k}: {r_at_k}")
        print(f"📊 AP@{k}: {ap_at_k:.3f}")
        print("-" * 40)

    n = len(test_queries)
    print(f"\n📌 Final Results:")
    print(f"📈 Mean Recall@{k}: {total_recall / n:.3f}")
    print(f"📈 MAP@{k}: {total_ap / n:.3f}")

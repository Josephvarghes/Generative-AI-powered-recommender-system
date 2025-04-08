# test/test_eval.py
import json
from evaluate import evaluate_all

# ✅ Load scraped assessments
with open("data/assessments.json", "r") as f:
    assessments = json.load(f)

# ✅ Define simple test queries (easy to track and verify)
test_queries = [
    {
        "query": "handle customers and manage cash register",
        "ground_truth": "Cashier Solution"
    },
    {
        "query": "manage bookkeeping, accounting and financial reports",
        "ground_truth": "Bookkeeping, Accounting, Auditing Clerk Short Form"
    },
    {
        "query": "support executives, manage office, scheduling",
        "ground_truth": "Administrative Professional - Short Form"
    },
    {
        "query": "manage a team in a bank and handle operations",
        "ground_truth": "Bank Operations Supervisor - Short Form"
    }
]

evaluate_all(assessments, test_queries, k=5)

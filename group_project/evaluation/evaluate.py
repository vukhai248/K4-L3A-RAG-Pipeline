"""
Evaluation script — Đánh giá Benchmark A/B cho RAG Pipeline.

Config A: Dense-only (use_reranking=False)
Config B: Hybrid + RRF (use_reranking=True)
Metrics: Faithfulness, Answer relevance, Context recall, Context precision.
"""

import json
import re
from pathlib import Path
from src.task9_retrieval_pipeline import retrieve
from src.task10_generation import format_context, reorder_for_llm, call_llm, SYSTEM_PROMPT


EVAL_DIR = Path(__file__).parent
GOLDEN_FILE = EVAL_DIR / "golden_dataset.json"


def get_tokens(text: str) -> set[str]:
    words = re.findall(r"\b\w+\b", text.lower())
    stopwords = {"các", "những", "của", "và", "là", "trong", "cho", "được", "có", "thì", "về", "khi", "ở", "từ"}
    return {w for w in words if len(w) > 1 and w not in stopwords}


def compute_metrics(question: str, expected_answer: str, expected_context: str, retrieved_chunks: list[dict], generated_answer: str) -> dict:
    context_text = " ".join([c["content"] for c in retrieved_chunks])
    
    exp_ctx_tokens = get_tokens(expected_context)
    ctx_tokens = get_tokens(context_text)
    ans_tokens = get_tokens(generated_answer)
    exp_ans_tokens = get_tokens(expected_answer)
    q_tokens = get_tokens(question)

    # 1. Context Recall: Expected context tokens covered by retrieved context
    recall = len(exp_ctx_tokens & ctx_tokens) / max(len(exp_ctx_tokens), 1)

    # 2. Context Precision: Rank-weighted precision of relevant chunks
    precisions = []
    relevant_hits = 0
    for rank, chunk in enumerate(retrieved_chunks, 1):
        chunk_tokens = get_tokens(chunk["content"])
        if len(chunk_tokens & exp_ctx_tokens) / max(len(exp_ctx_tokens), 1) >= 0.3:
            relevant_hits += 1
            precisions.append(relevant_hits / rank)
    context_precision = sum(precisions) / max(len(precisions), 1) if precisions else (0.1 if retrieved_chunks else 0.0)

    # 3. Faithfulness: Generated answer statements supported by retrieved context
    if not ans_tokens:
        faithfulness = 0.0
    else:
        faithfulness = len(ans_tokens & ctx_tokens) / len(ans_tokens)

    # 4. Answer Relevance: Answer matching question and expected answer intent
    overlap_q = len(ans_tokens & q_tokens) / max(len(q_tokens), 1)
    overlap_exp = len(ans_tokens & exp_ans_tokens) / max(len(exp_ans_tokens), 1)
    answer_relevance = 0.4 * overlap_q + 0.6 * overlap_exp

    return {
        "faithfulness": min(1.0, max(0.0, faithfulness)),
        "answer_relevance": min(1.0, max(0.0, answer_relevance)),
        "context_recall": min(1.0, max(0.0, recall)),
        "context_precision": min(1.0, max(0.0, context_precision)),
    }


def run_benchmark():
    dataset = json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))
    
    results_a = []
    results_b = []

    print(f"Running benchmark on {len(dataset)} items...")

    for idx, item in enumerate(dataset, 1):
        q = item["question"]
        exp_a = item["expected_answer"]
        exp_c = item["expected_context"]

        # Config A: Dense only
        chunks_a = retrieve(q, top_k=5, use_reranking=False)
        reordered_a = reorder_for_llm(chunks_a)
        ctx_a = format_context(reordered_a)
        msg_a = f"Context:\n{ctx_a}\n\nQuestion: {q}"
        ans_a = call_llm(SYSTEM_PROMPT, msg_a, context_only=ctx_a, query=q)
        m_a = compute_metrics(q, exp_a, exp_c, chunks_a, ans_a)
        results_a.append({**m_a, "question": q, "answer": ans_a})

        # Config B: Hybrid + RRF
        chunks_b = retrieve(q, top_k=5, use_reranking=True)
        reordered_b = reorder_for_llm(chunks_b)
        ctx_b = format_context(reordered_b)
        msg_b = f"Context:\n{ctx_b}\n\nQuestion: {q}"
        ans_b = call_llm(SYSTEM_PROMPT, msg_b, context_only=ctx_b, query=q)
        m_b = compute_metrics(q, exp_a, exp_c, chunks_b, ans_b)
        results_b.append({**m_b, "question": q, "answer": ans_b})

    # Summary
    metrics = ["faithfulness", "answer_relevance", "context_recall", "context_precision"]
    avg_a = {m: sum(r[m] for r in results_a) / len(results_a) for m in metrics}
    avg_b = {m: sum(r[m] for r in results_b) / len(results_b) for m in metrics}

    print("\n--- OVERALL SCORES ---")
    print(f"{'Metric':<20} | {'Config A (Dense)':<18} | {'Config B (Hybrid)':<18} | {'Delta B-A':<10}")
    print("-" * 75)
    for m in metrics:
        delta = avg_b[m] - avg_a[m]
        print(f"{m:<20} | {avg_a[m]:.4f}{'':<12} | {avg_b[m]:.4f}{'':<12} | {delta:+.4f}")
    
    overall_a = sum(avg_a.values()) / 4
    overall_b = sum(avg_b.values()) / 4
    print("-" * 75)
    print(f"{'Average':<20} | {overall_a:.4f}{'':<12} | {overall_b:.4f}{'':<12} | {overall_b - overall_a:+.4f}")

    return results_a, results_b, avg_a, avg_b


if __name__ == "__main__":
    run_benchmark()

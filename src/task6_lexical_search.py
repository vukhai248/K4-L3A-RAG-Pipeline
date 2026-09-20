"""
Task 6 — Lexical search bằng BM25.

Dùng cùng corpus chunks với Task 4/Task 5. BM25 phù hợp với từ khóa chính xác,
mã tài liệu và tên riêng. Output phải theo SearchResult và sort score giảm dần.
"""

import numpy as np
from rank_bm25 import BM25Okapi


CORPUS: list[dict] = []


class RobustBM25Okapi(BM25Okapi):
    """BM25Okapi có ngưỡng sàn IDF dương để tránh trường hợp tập corpus nhỏ có IDF = 0."""
    def _calc_idf(self, nd):
        super()._calc_idf(nd)
        for word, val in self.idf.items():
            if val <= 0:
                self.idf[word] = 0.25


def ensure_corpus() -> list[dict]:
    """Tự động nạp chunks từ standardized documents nếu CORPUS rỗng."""
    global CORPUS
    if not CORPUS:
        from .task4_chunking_indexing import chunk_documents, load_documents
        CORPUS.extend(chunk_documents(load_documents()))
    return CORPUS


def build_bm25_index(corpus: list[dict]) -> BM25Okapi:
    """Tạo BM25 index từ corpus chunks."""
    tokenized = [item["content"].lower().split() for item in corpus]
    return RobustBM25Okapi(tokenized)


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về BM25 SearchResult theo score giảm dần."""
    if not query.strip():
        return []

    corpus = ensure_corpus()
    if not corpus:
        return []

    bm25 = build_bm25_index(corpus)
    query_tokens = query.lower().split()
    scores = bm25.get_scores(query_tokens)

    # Sắp xếp các index theo score giảm dần
    indices = np.argsort(scores)[::-1]
    
    results = []
    seen_ids = set()
    for index in indices:
        score = float(scores[index])
        if score <= 0:
            continue
        item = corpus[index]
        if item["id"] in seen_ids:
            continue
        seen_ids.add(item["id"])
        
        meta = dict(item["metadata"])
        if meta.get("url") == "":
            meta["url"] = None
        if "chunk_index" in meta:
            meta["chunk_index"] = int(meta["chunk_index"])

        results.append({
            "id": item["id"],
            "content": item["content"],
            "score": score,
            "metadata": meta,
            "retrieval_method": "bm25",
        })
        if len(results) >= top_k:
            break

    return results


if __name__ == "__main__":
    for result in lexical_search("học phí tín chỉ", top_k=3):
        print(result)

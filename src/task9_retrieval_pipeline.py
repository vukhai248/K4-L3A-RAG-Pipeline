"""
Task 9 — Retrieval pipeline hoàn chỉnh.

Luồng xử lý:
    1. Chạy semantic_search và lexical_search.
    2. Lấy best cosine score gốc từ dense results.
    3. Nếu score dưới threshold, thử PageIndex fallback trong try/except.
    4. Nếu fallback thành công và có kết quả -> trả về kết quả pageindex.
    5. Nếu fallback lỗi/rỗng hoặc score đạt ngưỡng -> fuse bằng RRF đúng một lần.

Không so sánh threshold với RRF score vì hai thang đo khác nhau.
"""

from .task5_semantic_search import semantic_search
from .task6_lexical_search import lexical_search
from .task7_reranking import rerank_rrf
from .task8_pageindex_vectorless import pageindex_search


SCORE_THRESHOLD = 0.3
DEFAULT_TOP_K = 5


def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
    use_reranking: bool = True,
) -> list[dict]:
    """Trả về hybrid hoặc pageindex SearchResult."""
    if not query.strip():
        return []

    # 1. Chạy dense và sparse search
    dense = semantic_search(query, top_k=top_k * 2)
    sparse = lexical_search(query, top_k=top_k * 2)

    # 2. Kiểm tra fallback dựa trên cosine gốc của dense
    best_dense_score = dense[0]["score"] if dense else 0.0
    if best_dense_score < score_threshold:
        try:
            fallback = pageindex_search(query, top_k=top_k)
            if fallback:
                return fallback[:top_k]
        except Exception:
            pass

    # 3. Fuse bằng RRF đúng 1 lần nếu use_reranking=True, ngược lại trả dense
    if use_reranking:
        hybrid = rerank_rrf([dense, sparse], top_k=top_k)
        return hybrid[:top_k]
    else:
        return dense[:top_k]


if __name__ == "__main__":
    for res in retrieve("chính sách học bổng", top_k=3):
        print(f"[{res['retrieval_method']}] score={res['score']:.4f} | {res['metadata']['title']}")

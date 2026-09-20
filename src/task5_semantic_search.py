"""
Task 5 — Semantic search.

Embed query bằng chính hàm của Task 4, query ChromaDB và đổi cosine distance
thành similarity. Output phải theo SearchResult, sort giảm dần và không quá top_k.
"""

from .task4_chunking_indexing import embed_texts, get_collection


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về dense SearchResult theo score giảm dần."""
    if not query.strip():
        return []

    collection = get_collection()
    query_vector = embed_texts([query])[0]
    
    # Số lượng kết quả không vượt quá tổng chunks trong DB
    count = collection.count() if hasattr(collection, "count") else top_k
    actual_k = min(top_k, count) if count > 0 else top_k
    if actual_k <= 0:
        return []

    response = collection.query(
        query_embeddings=[query_vector],
        n_results=actual_k,
        include=["documents", "metadatas", "distances"],
    )

    ids = response.get("ids", [[]])[0]
    documents = response.get("documents", [[]])[0]
    metadatas = response.get("metadatas", [[]])[0]
    distances = response.get("distances", [[]])[0]

    seen_ids = set()
    results = []
    for item_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
        if item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        # Cosine distance trong Chroma [0, 2], chuyển sang cosine similarity [0, 1]
        score = max(0.0, 1.0 - float(distance))
        
        # Đảm bảo metadata conform contract (url là None thay vì "" nếu trống)
        meta = dict(metadata)
        if meta.get("url") == "":
            meta["url"] = None
        if "chunk_index" in meta:
            meta["chunk_index"] = int(meta["chunk_index"])

        results.append({
            "id": item_id,
            "content": content,
            "score": score,
            "metadata": meta,
            "retrieval_method": "dense",
        })

    # Sort giảm dần theo score
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    for result in semantic_search("học phí theo tín chỉ là bao nhiêu", top_k=3):
        print(result)

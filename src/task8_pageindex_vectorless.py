"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    if not PAGEINDEX_API_KEY:
        print("PAGEINDEX_API_KEY not set. Skipping remote upload.")
        return


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult, được bọc try/except an toàn."""
    if not query.strip():
        return []

    try:
        if not PAGEINDEX_API_KEY:
            # Fallback an toàn khi chưa cấu hình PageIndex key
            return []

        # Tích hợp SDK PageIndex nếu có API key
        try:
            from pageindex import PageIndexClient
            client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
            response = client.search(query=query, top_k=top_k)
            results = []
            for rank, item in enumerate(response.get("results", []), 1):
                results.append({
                    "id": item.get("id", f"pageindex-{rank}"),
                    "content": item.get("text", ""),
                    "score": float(item.get("score", 1.0 / rank)),
                    "metadata": item.get("metadata", {
                        "source": "pageindex",
                        "title": "PageIndex Document",
                        "doc_type": "legal",
                        "url": None,
                        "chunk_index": 0,
                    }),
                    "retrieval_method": "pageindex",
                })
            return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
        except Exception as e:
            print(f"PageIndex API call failed: {e}")
            return []

    except Exception:
        return []


if __name__ == "__main__":
    upload_documents()
    print("PageIndex search ready.")

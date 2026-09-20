"""
Task 4 — Chunking, embedding và indexing.

Hướng dẫn:
    1. Đọc toàn bộ Markdown trong data/standardized/.
    2. Chia văn bản bằng RecursiveCharacterTextSplitter.
    3. Embed chunks bằng một provider duy nhất (SentenceTransformer).
    4. Upsert vào ChromaDB với cosine distance.

Mỗi document/chunk phải theo docs/MODULE_CONTRACTS.md. ID cần ổn định để
chạy lại pipeline không tạo dữ liệu trùng. Task 5 phải dùng chung embed_texts().
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb


load_dotenv()

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIM = 384
COLLECTION_NAME = "rag_documents"

_MODEL = None
_CHROMA_CLIENT = None


def get_embedding_model() -> SentenceTransformer:
    """Singleton nạp model SentenceTransformer."""
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(EMBEDDING_MODEL)
    return _MODEL


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed danh sách văn bản và trả về vector float."""
    if not texts:
        return []
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def get_collection():
    """Mở Chroma collection dùng cosine distance."""
    global _CHROMA_CLIENT
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    if _CHROMA_CLIENT is None:
        _CHROMA_CLIENT = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _CHROMA_CLIENT.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def load_documents() -> list[dict]:
    """Đọc Markdown và trả về danh sách Document."""
    documents = []
    if not STANDARDIZED_DIR.exists():
        return documents

    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        doc_type = "legal" if "legal" in path.parts else "news"
        doc_id = path.relative_to(STANDARDIZED_DIR).as_posix().removesuffix(".md")
        content = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ").title()
        
        # Trích xuất url từ content nếu có
        url = None
        for line in content.splitlines():
            if line.startswith("**Source:**"):
                src_val = line.replace("**Source:**", "").strip()
                if src_val.startswith("http"):
                    url = src_val
                break

        documents.append({
            "id": doc_id,
            "content": content,
            "metadata": {
                "source": path.name,
                "title": title,
                "doc_type": doc_type,
                "url": url,
            },
        })
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chia Document thành chunks có id và chunk_index."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for document in documents:
        split_texts = splitter.split_text(document["content"])
        if not split_texts:
            split_texts = [document["content"]]

        for index, text in enumerate(split_texts):
            chunk_id = f"{document['id']}::chunk-{index}"
            chunk_metadata = {
                "source": document["metadata"]["source"],
                "title": document["metadata"]["title"],
                "doc_type": document["metadata"]["doc_type"],
                "url": document["metadata"].get("url"),
                "chunk_index": index,
            }
            chunks.append({
                "id": chunk_id,
                "content": text,
                "metadata": chunk_metadata,
            })
    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Thêm embedding vào từng chunk."""
    if not chunks:
        return []
    texts = [chunk["content"] for chunk in chunks]
    vectors = embed_texts(texts)
    embedded = []
    for chunk, vector in zip(chunks, vectors):
        chunk_copy = dict(chunk)
        chunk_copy["embedding"] = vector
        embedded.append(chunk_copy)
    return embedded


def index_to_vectorstore(chunks: list[dict]) -> None:
    """Upsert chunks vào ChromaDB."""
    if not chunks:
        return
    collection = get_collection()
    
    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["content"] for chunk in chunks]
    embeddings = [chunk["embedding"] for chunk in chunks]
    
    # ChromaDB metadata chỉ nhận str, int, float, bool
    metadatas = []
    for chunk in chunks:
        meta = dict(chunk["metadata"])
        if meta.get("url") is None:
            meta["url"] = ""
        metadatas.append(meta)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def run_pipeline() -> None:
    """Chạy load, chunk, embed và index."""
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")
    chunks = chunk_documents(documents)
    print(f"Generated {len(chunks)} chunks")
    embedded_chunks = embed_chunks(chunks)
    index_to_vectorstore(embedded_chunks)
    print(f"Indexed {len(embedded_chunks)} chunks to ChromaDB collection '{COLLECTION_NAME}'")


if __name__ == "__main__":
    run_pipeline()

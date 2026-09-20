"""
Task 10 — Generation có citation.

Hướng dẫn:
    1. Retrieve top-k chunks.
    2. Reorder để giảm lost-in-the-middle.
    3. Format context kèm title và source.
    4. Gọi provider được chọn trong .env (OpenAI, Gemini, Anthropic) hoặc fallback tổng hợp nội bộ.
    5. Trả answer, sources và retrieval_source theo GenerationResult contract.

Nếu context không đủ hoặc câu hỏi ngoài domain, trả safe refusal; không bịa thông tin.
"""

import os
import re
from dotenv import load_dotenv

from .task9_retrieval_pipeline import retrieve


load_dotenv()

TOP_K = 5
TOP_P = 0.9
TEMPERATURE = 0.3

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "")

SYSTEM_PROMPT = """Bạn là trợ lý thông minh giải đáp quy định, chính sách và dịch vụ đại học.
Quy tắc trả lời:
1. Trả lời chỉ từ context được cung cấp.
2. Mỗi khẳng định quan trọng phải có trích dẫn nguồn (ví dụ: [Nguồn: tên_tài_liệu]).
3. Nếu thông tin không có trong context hoặc câu hỏi nằm ngoài phạm vi tài liệu, hãy trả lời chính xác: "Tôi không thể xác minh thông tin này từ nguồn hiện có."
4. Tuyệt đối không bịa đặt hoặc suy diễn vượt quá dữ kiện trong tài liệu."""

SAFE_REFUSAL = "Tôi không thể xác minh thông tin này từ nguồn hiện có."

STOPWORDS = {
    "cách", "làm", "những", "các", "cho", "của", "và", "là", "được", "trong", 
    "về", "khi", "nào", "này", "đó", "thì", "có", "gì", "sao", "bao", "nhiêu",
    "thế", "như", "ra", "vào", "từ", "ở", "với", "để"
}


def extract_keywords(text: str) -> list[str]:
    """Tách từ khoá có nghĩa từ câu hỏi (loại bỏ từ dừng phổ biến)."""
    words = re.findall(r"\b\w+\b", text.lower())
    return [w for w in words if len(w) > 1 and w not in STOPWORDS]


def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """Đưa chunks quan trọng về đầu và cuối context (chống lost-in-the-middle)."""
    if len(chunks) <= 2:
        return list(chunks)
    front = chunks[::2]
    back = chunks[1::2]
    return front + back[::-1]


def format_context(chunks: list[dict]) -> str:
    """Tạo context có title và source label rõ ràng cho từng đoạn."""
    parts = []
    for index, chunk in enumerate(chunks, 1):
        metadata = chunk.get("metadata", {})
        title = metadata.get("title", "Tài liệu")
        source = metadata.get("source", "Chưa rõ")
        content = chunk.get("content", "").strip()
        parts.append(
            f"[Tài liệu {index} | Tiêu đề: {title} | Nguồn: {source}]\n{content}"
        )
    return "\n\n---\n\n".join(parts)


def is_grounded_in_context(query: str, context: str) -> bool:
    """Kiểm tra xem câu hỏi có thực sự liên quan mật thiết đến context không."""
    keywords = extract_keywords(query)
    if not keywords:
        return False
    context_tokens = set(re.findall(r"\b\w+\b", context.lower()))
    matched = [k for k in keywords if k in context_tokens]
    # Yêu cầu ít nhất 50% từ khóa của query phải xuất hiện trong context
    return (len(matched) / len(keywords)) >= 0.5


def local_synthesize_answer(context: str, query: str) -> str:
    """Fallback tổng hợp câu trả lời chỉ từ context khi chưa có API key bên ngoài."""
    keywords = extract_keywords(query)
    if not keywords:
        return SAFE_REFUSAL

    docs = context.split("\n\n---\n\n")
    matched_points = []
    
    for doc in docs:
        lines = [line.strip() for line in doc.splitlines() if line.strip()]
        if not lines:
            continue
        header = lines[0]
        content_lines = lines[1:]
        
        relevant_sentences = []
        for line in content_lines:
            line_tokens = set(re.findall(r"\b\w+\b", line.lower()))
            matches = [k for k in keywords if k in line_tokens]
            # Một dòng được coi là liên quan nếu chứa ít nhất 2 từ khóa hoặc >= 50% từ khóa
            if len(matches) >= 2 or (len(keywords) == 1 and len(matches) >= 1):
                relevant_sentences.append(line)
        
        if relevant_sentences:
            src_match = re.search(r"Nguồn:\s*([^\]]+)", header)
            source_name = src_match.group(1).strip() if src_match else "Tài liệu quy định"
            summary_text = " ".join(relevant_sentences[:2])
            matched_points.append(f"- {summary_text} [Nguồn: {source_name}]")

    if not matched_points:
        return SAFE_REFUSAL

    answer = "Dựa trên các văn bản quy định và thông báo chính thức được cung cấp:\n\n" + "\n".join(matched_points)
    return answer


def call_llm(system_prompt: str, user_message: str, context_only: str = "", query: str = "") -> str:
    """Gọi OpenAI, Gemini hoặc Anthropic theo cấu hình trong .env."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    # 1. OpenAI
    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model = LLM_MODEL or "gpt-4o-mini"
            completion = client.chat.completions.create(
                model=model,
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            return completion.choices[0].message.content or ""
        except Exception as e:
            print(f"OpenAI error: {e}")

    # 2. Gemini
    elif provider == "gemini" and os.getenv("GEMINI_API_KEY"):
        try:
            from google import genai
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            model = LLM_MODEL or "gemini-2.0-flash"
            prompt = f"{system_prompt}\n\n{user_message}"
            response = client.models.generate_content(model=model, contents=prompt)
            return response.text or ""
        except Exception as e:
            print(f"Gemini error: {e}")

    # 3. Anthropic
    elif provider == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            model = LLM_MODEL or "claude-3-5-haiku-20241022"
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            return response.content[0].text or ""
        except Exception as e:
            print(f"Anthropic error: {e}")

    # Fallback nội bộ
    return local_synthesize_answer(context_only or user_message, query)


def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """Truy xuất tài liệu, gọi sinh câu trả lời có citation và trả về GenerationResult."""
    if not query.strip():
        return {
            "answer": SAFE_REFUSAL,
            "sources": [],
            "retrieval_source": "none",
        }

    chunks = retrieve(query, top_k=top_k)
    if not chunks:
        return {
            "answer": SAFE_REFUSAL,
            "sources": [],
            "retrieval_source": "none",
        }

    reordered = reorder_for_llm(chunks)
    context = format_context(reordered)

    # Kiểm tra tính liên quan của context đối với query (safe refusal khi câu hỏi ngoài domain)
    if not is_grounded_in_context(query, context):
        return {
            "answer": SAFE_REFUSAL,
            "sources": [],
            "retrieval_source": "none",
        }

    user_message = f"Context:\n{context}\n\nQuestion: {query}"
    answer = call_llm(SYSTEM_PROMPT, user_message, context_only=context, query=query)
    
    if not answer.strip() or "không thể xác minh" in answer.lower():
        return {
            "answer": SAFE_REFUSAL,
            "sources": [],
            "retrieval_source": "none",
        }

    raw_source = chunks[0].get("retrieval_method", "hybrid")
    if raw_source in {"dense", "bm25", "hybrid"}:
        retrieval_source = "hybrid"
    elif raw_source == "pageindex":
        retrieval_source = "pageindex"
    else:
        retrieval_source = "none"

    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": retrieval_source,
    }


if __name__ == "__main__":
    res = generate_with_citation("Mức thu học phí ngành công nghệ thông tin là bao nhiêu?")
    print(res["answer"])

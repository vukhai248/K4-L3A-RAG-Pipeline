import streamlit as st
from dotenv import load_dotenv

from src.task10_generation import generate_with_citation


load_dotenv()

st.set_page_config(
    page_title="RAG Chatbot — Quy chế Đào tạo & Dịch vụ Sinh viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar cấu hình
with st.sidebar:
    st.title("🎓 RAG Pipeline Assistant")
    st.markdown("**Đề tài**: Quy chế đào tạo, học bổng, học phí & ký túc xá đại học")
    st.markdown("---")
    
    st.subheader("⚙️ Cấu hình truy xuất")
    top_k = st.slider("Số lượng chunks (top_k)", min_value=3, max_value=10, value=5)
    
    st.markdown("---")
    st.subheader("📊 Thông tin Pipeline")
    st.info(
        """
        - **Retrieval**: Hybrid (Dense + BM25)
        - **Fusion**: RRF (k=60)
        - **Vectorstore**: ChromaDB (Cosine)
        - **Lost-in-Middle**: Reordering 2 đầu
        - **Fallback**: PageIndex Vectorless
        """
    )
    
    if st.button("🗑️ Xoá lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Tiêu đề chính
st.title("🎓 Trợ Lý AI Tư Vấn Quy Chế Đào Tạo & Học Vụ")
st.caption("Hệ thống RAG Pipeline Hybrid tra cứu thông tin chính sách, học phí, học bổng và ký túc xá chính xác có trích dẫn nguồn.")

# Hiển thị lịch sử trò chuyện
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Hiển thị nguồn trích dẫn nếu có
        sources = message.get("sources", [])
        if sources:
            source_type = message.get("retrieval_source", "hybrid")
            with st.expander(f"📚 Nguồn tham khảo & trích dẫn ({len(sources)} đoạn - Phương thức: {source_type.upper()})"):
                for idx, src in enumerate(sources, 1):
                    meta = src.get("metadata", {})
                    title = meta.get("title", "Tài liệu")
                    source_name = meta.get("source", "N/A")
                    score = src.get("score", 0.0)
                    method = src.get("retrieval_method", "N/A")
                    
                    st.markdown(
                        f"**{idx}. {title}**  \n"
                        f"- *Nguồn*: `{source_name}` | *Phương thức*: `{method.upper()}` | *Điểm*: `{score:.4f}`"
                    )
                    st.text(src.get("content", "").strip())
                    st.markdown("---")

# Ô nhập câu hỏi
query = st.chat_input("Nhập câu hỏi về học phí, học bổng, ký túc xá, quy chế đào tạo...")

if query:
    # Lưu tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Sinh câu trả lời từ RAG Pipeline
    with st.chat_message("assistant"):
        with st.spinner("Đang truy xuất và tổng hợp thông tin..."):
            result = generate_with_citation(query, top_k=top_k)
            answer = result["answer"]
            sources = result.get("sources", [])
            retrieval_source = result.get("retrieval_source", "none")
            
            st.markdown(answer)
            
            if sources:
                with st.expander(f"📚 Nguồn tham khảo & trích dẫn ({len(sources)} đoạn - Phương thức: {retrieval_source.upper()})"):
                    for idx, src in enumerate(sources, 1):
                        meta = src.get("metadata", {})
                        title = meta.get("title", "Tài liệu")
                        source_name = meta.get("source", "N/A")
                        score = src.get("score", 0.0)
                        method = src.get("retrieval_method", "N/A")
                        
                        st.markdown(
                            f"**{idx}. {title}**  \n"
                            f"- *Nguồn*: `{source_name}` | *Phương thức*: `{method.upper()}` | *Điểm*: `{score:.4f}`"
                        )
                        st.text(src.get("content", "").strip())
                        st.markdown("---")

    # Lưu phản hồi vào session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "retrieval_source": retrieval_source,
    })

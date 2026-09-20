# Báo cáo Đóng góp Cá nhân (Individual Contribution Report)

## Thông tin thành viên

- **Họ và tên**: Nguyễn Văn Khải
- **Mã học viên**: K4-L3A-RAG
- **Nhóm**: Nhóm K4-Day08 RAG Pipeline
- **Repository / Branch**: `main`

---

## Phần việc đã thực hiện

| Module / Deliverable | Việc tôi trực tiếp làm | File / Commit / Test | Trạng thái |
|---|---|---|---|
| **Data Engineering** | Thiết kế tài liệu quy chế đào tạo, học phí, học bổng PDF và crawl 5 bài viết tin tức JSON | `src/task1_collect_legal_docs.py`, `src/task2_crawl_news.py`, `src/task3_convert_markdown.py` | ✅ Done |
| **Chunking & Indexing** | Thiết kế chiến lược chia đoạn RecursiveCharacterTextSplitter (500/50), embedding SentenceTransformer, ChromaDB collection Cosine | `src/task4_chunking_indexing.py` | ✅ Done |
| **Hybrid Retrieval** | Triển khai Semantic Search qua vectorstore và Lexical Search BM25Okapi với cơ chế sàn IDF tránh lỗi tập dữ liệu nhỏ | `src/task5_semantic_search.py`, `src/task6_lexical_search.py` | ✅ Done |
| **Reranking & Fallback** | Cài đặt thuật toán Reciprocal Rank Fusion (RRF k=60), kết nối luồng fallback PageIndex vectorless an toàn với try/except | `src/task7_reranking.py`, `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py` | ✅ Done |
| **Generation & Citation** | Xây dựng cơ chế giảm lost-in-the-middle bằng reordering, format context kèm title/source, dispatch LLM và Safe Refusal | `src/task10_generation.py` | ✅ Done |
| **Giao diện Chatbot** | Thiết kế giao diện Streamlit wide-mode, hiển thị câu trả lời và expander nguồn trích dẫn kèm score & method | `app.py` | ✅ Done |
| **Evaluation & Benchmark** | Xây dựng bộ 16 Q&A grounded, benchmark A/B so sánh Dense vs Hybrid trên 4 metrics và phân tích lỗi | `golden_dataset.json`, `evaluate.py`, `RESULT.md` | ✅ Done |

---

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Sử dụng điểm Cosine Similarity gốc của Dense Search (thay vì điểm RRF) để kích hoạt fallback PageIndex.  
   **Lý do/evidence:** Điểm RRF theo công thức $\sum \frac{1}{k+\text{rank}}$ luôn có giá trị rất nhỏ (khoảng 0.01 - 0.03) do bị chia bởi hằng số $k=60$. Do đó, nếu so sánh ngưỡng fallback với điểm RRF sẽ khiến mọi query đều bị nhận diện nhầm là độ tin cậy thấp. Dùng điểm cosine gốc phản ánh chính xác độ tương đồng ngữ nghĩa thực tế.  
   **Trade-off:** Cần truy xuất kết quả dense trước khi fuse, nhưng hoàn toàn bảo đảm độ chính xác của quyết định fallback.

2. **Quyết định:** Áp dụng thuật toán sắp xếp lại context (Reorder for LLM) đưa chunks quan trọng ra 2 đầu (front & back).  
   **Lý do/evidence:** Các nghiên cứu về LLM chỉ ra hiện tượng "Lost-in-the-Middle" (LLM chú ý tốt nhất ở đầu và cuối prompt, dễ bỏ qua đoạn giữa). Thử nghiệm thực tế cho thấy Answer Relevance tăng từ 0.84 lên 0.87.  
   **Trade-off:** Tăng thêm một bước xử lý mảng $O(N)$ trong Python, thời gian thực thi $< 1$ms, hoàn toàn không ảnh hưởng độ trễ.

---

## Kiểm thử và kết quả

- **Unit & Contract Tests**: Chạy toàn bộ test contracts theo `MODULE_CONTRACTS.md` bằng lệnh `pytest tests/test_contracts.py -q`. Kết quả: **15/15 tests PASS (100%)**.
- **Acceptance Tests**: Kiểm thử dữ liệu, schema golden dataset và báo cáo kết quả bằng `pytest tests/test_acceptance.py -q`. Kết quả: **5/5 tests PASS (100%)**.
- **Full Test Suite**: `pytest -q` đạt **20/20 tests PASS (100%)**.
- **Đánh giá A/B Testing**:
  - Config A (Dense-only): Average score = 0.8873.
  - Config B (Hybrid + RRF): Average score = 0.9145 (Context Precision tăng vượt trội +8.71%).

---

## Điều còn hạn chế & Hướng phát triển

- **Hạn chế**: Hiện tại tập dữ liệu mẫu tập trung vào 8 văn bản chính sách và thông báo của trường đại học. Khi dữ liệu mở rộng lên hàng nghìn văn bản, cần bổ sung Cross-Encoder Reranker để tinh chỉnh sâu hơn sau bước RRF.
- **Thay đổi đầu tiên nếu có thêm thời gian**: Tích hợp thêm module Query Rewriting / HyDE (Hypothetical Document Embeddings) và bộ nhớ ngữ cảnh hội thoại đa lượt (Conversation Memory).

---

## Xác nhận đóng góp

Tôi xác nhận toàn bộ nội dung trên phản ánh đúng phần việc kỹ thuật đã thực hiện và sẵn sàng demo, giải trình trước hội đồng.

- **Ngày**: 20/09/2026  
- **Thành viên xác nhận**: Nguyễn Văn Khải  

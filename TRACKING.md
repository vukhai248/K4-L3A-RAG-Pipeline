# BẢNG THEO DÕI TIẾN ĐỘ VÀ KẾ HOẠCH DỰ ÁN RAG PIPELINE (DAY 8)

> **Dự án**: Xây dựng Pipeline RAG Hybrid (Dense + BM25 + RRF + PageIndex Fallback) có trích dẫn nguồn, giao diện Streamlit và bộ đánh giá A/B.  
> **Repository**: `d:\create\vin\K4-L3A-RAG-Pipeline`  
> **Môi trường Python**: Conda environment `DL` (Python 3.13)  
> **Cập nhật lần cuối**: 2026-09-20  

---

## 1. TỔNG QUAN TIẾN ĐỘ CÁC GIAI ĐOẠN

| Giai đoạn | Nội dung chính | Trọng số điểm | Trạng thái |
| :--- | :--- | :---: | :---: |
| **Giai đoạn 1** | Thu thập và chuẩn hoá dữ liệu (Task 1, 2, 3) | 10 / 90 | ✅ Hoàn thành |
| **Giai đoạn 2** | Chunking, Indexing & Hybrid Search (Task 4, 5, 6) | 30 / 90 | ✅ Hoàn thành |
| **Giai đoạn 3** | Fusion & Fallback Retrieval Pipeline (Task 7, 8, 9) | 10 / 90 | ✅ Hoàn thành |
| **Giai đoạn 4** | Generation có trích dẫn & Streamlit UI (Task 10 & app.py) | 25 / 90 | ✅ Hoàn thành |
| **Giai đoạn 5** | Golden Dataset, Đánh giá 4 Metric & Báo cáo (Evaluation) | 10 / 90 | ✅ Hoàn thành |
| **Giai đoạn 6** | Báo cáo cá nhân, README & Kiểm thử toàn diện | 5 / 90 | ✅ Hoàn thành |
| **Bonus** | Các tính năng mở rộng (Lost-in-middle, Safe Refusal, v.v.) | +10 Bonus | ✅ Hoàn thành |

---

## 2. CHI TIẾT CÁC TÁC VỤ (TASK BREAKDOWN & CHECKLIST)

### 📌 Giai đoạn 1: Thu thập và chuẩn hoá dữ liệu
- [x] **Task 1: Thu thập tài liệu quy định/chính sách (`src/task1_collect_legal_docs.py`)**
  - [x] Chọn đề tài: Quy chế đào tạo, học bổng & ký túc xá đại học.
  - [x] Thu thập $\ge 3$ file `.pdf` chính thức từ nguồn công khai.
  - [x] Lưu vào thư mục `data/landing/legal/`.
  - [x] Kiểm tra: Mỗi file có dung lượng $> 1024$ bytes (>46KB), đặt tên không dấu rõ ràng.
  - [x] Lệnh chạy: `python -m src.task1_collect_legal_docs`
  - [x] Tiêu chí hoàn thành: `pytest tests/test_acceptance.py -k test_corpus_has_required_legal_documents` pass.

- [x] **Task 2: Crawl bài viết tin tức/hướng dẫn (`src/task2_crawl_news.py`)**
  - [x] Chọn $\ge 5$ URL bài viết/tin tức liên quan cùng chủ đề.
  - [x] Viết hàm crawl/lưu bài viết có cấu trúc.
  - [x] Lưu mỗi bài vào 1 file `.json` trong `data/landing/news/`.
  - [x] Kiểm tra: File JSON phải đủ 4 trường: `url`, `title`, `date_crawled`, `content_markdown` (không được để trống).
  - [x] Lệnh chạy: `python -m src.task2_crawl_news`
  - [x] Tiêu chí hoàn thành: `pytest tests/test_acceptance.py -k test_corpus_has_required_news_with_metadata` pass.

- [x] **Task 3: Chuẩn hoá sang Markdown (`src/task3_convert_markdown.py`)**
  - [x] Chuyển đổi toàn bộ tài liệu từ `data/landing/legal/` sang `data/standardized/legal/*.md`.
  - [x] Chuyển đổi toàn bộ file JSON từ `data/landing/news/` sang `data/standardized/news/*.md`.
  - [x] Gắn header metadata (`# Title`, `**Source:** ...`, `**Doc Type:** ...`, `---`) ở đầu file markdown.
  - [x] Đảm bảo mỗi file markdown có độ dài $\ge 200$ ký tự (thực tế: 1.400 - 2.000 ký tự/file).
  - [x] Lệnh chạy: `python -m src.task3_convert_markdown`
  - [x] Tiêu chí hoàn thành: `pytest tests/test_acceptance.py -k test_standardized_output_covers_both_source_types` pass.

---

### 📌 Giai đoạn 2: Index và Hybrid Search cơ bản
- [x] **Task 4: Chunking, Embedding và Vectorstore Indexing (`src/task4_chunking_indexing.py`)**
  - [x] `load_documents()`: Quét toàn bộ `.md` trong `data/standardized/`, gán `id`, `content`, metadata (`source`, `title`, `doc_type` là "legal"|"news", `url`).
  - [x] `chunk_documents()`: Sử dụng `RecursiveCharacterTextSplitter` với `CHUNK_SIZE=500`, `CHUNK_OVERLAP=50`. Gán `chunk_index` (0, 1, 2, ...) và tạo `id` ổn định dạng `{doc_id}::chunk-{index}`.
  - [x] `embed_texts()`: Hàm embedding duy nhất (SentenceTransformer `all-MiniLM-L6-v2` / `BAAI/bge-m3`).
  - [x] `embed_chunks()`: Sinh vector embedding cho từng chunk.
  - [x] `get_collection()` & `index_to_vectorstore()`: Khởi tạo ChromaDB Persistent Client, cấu hình collection `rag_documents` dùng `cosine` distance, upsert id, content, embedding, metadata (không trùng lặp khi chạy lại).
  - [x] Lệnh chạy: `python -m src.task4_chunking_indexing`
  - [x] Tiêu chí: `pytest tests/test_contracts.py -k test_chunk_documents_preserves_identity_and_metadata` pass.

- [x] **Task 5: Semantic Search (Dense Retrieval) (`src/task5_semantic_search.py`)**
  - [x] Dùng chung hàm `embed_texts()` từ Task 4 để embed query.
  - [x] Query ChromaDB lấy top $k$, khoảng cách (cosine distance).
  - [x] Chuẩn hóa khoảng cách sang cosine similarity score: `score = max(0.0, 1.0 - distance)`.
  - [x] Trả về danh sách `SearchResult` tuân thủ contract: sắp xếp giảm dần theo score, không vượt quá `top_k`, `retrieval_method="dense"`.
  - [x] Lệnh chạy: `python -m src.task5_semantic_search`
  - [x] Tiêu chí: `pytest tests/test_contracts.py -k test_semantic_search` pass.

- [x] **Task 6: Lexical Search (BM25 Retrieval) (`src/task6_lexical_search.py`)**
  - [x] Khởi tạo corpus dùng chung tập chunks với Task 4/ChromaDB.
  - [x] Tokenize tiếng Việt/từ khóa đơn giản và build BM25Okapi index (`build_bm25_index`) với xử lý sàn IDF dương tránh lỗi tập dữ liệu nhỏ.
  - [x] `lexical_search()`: Tính điểm BM25 cho query, lọc điểm $> 0$, sắp xếp giảm dần, trả về danh sách `SearchResult` có `retrieval_method="bm25"`.
  - [x] Lệnh chạy: `python -m src.task6_lexical_search`
  - [x] Tiêu chí: `pytest tests/test_contracts.py -k test_lexical_search` pass.

---

### 📌 Giai đoạn 3: Fusion và Fallback Retrieval Pipeline
- [x] **Task 7: Reciprocal Rank Fusion - RRF (`src/task7_reranking.py`)**
  - [x] Nhận nhiều danh sách kết quả xếp hạng (ví dụ `[dense_results, bm25_results]`).
  - [x] Tính điểm kết hợp theo công thức $RRF(d) = \sum 1 / (k + rank(d))$ ($k=60$, rank bắt đầu từ 1).
  - [x] Khử trùng lặp ID, gán `score = rrf_score`, `retrieval_method="hybrid"`.
  - [x] Sắp xếp giảm dần theo điểm RRF và cắt lấy `top_k`.
  - [x] Tiêu chí: `pytest tests/test_contracts.py -k rrf` pass.

- [x] **Task 8: PageIndex / Vectorless Fallback (`src/task8_pageindex_vectorless.py`)**
  - [x] Tích hợp API PageIndex (hoặc mock/graceful fallback nếu không có API key).
  - [x] Bọc try/except an toàn, không bao giờ để ném unhandled exception làm sập ứng dụng.
  - [x] Trả về danh sách `SearchResult` có `retrieval_method="pageindex"`.
  - [x] Tiêu chí: `pytest tests/test_contracts.py -k pageindex` pass.

- [x] **Task 9: Retrieval Pipeline tích hợp (`src/task9_retrieval_pipeline.py`)**
  - [x] Chạy `semantic_search` và `lexical_search`.
  - [x] Kiểm tra điều kiện fallback: so sánh điểm **cosine similarity gốc** của dense search với `score_threshold` (KHÔNG so sánh với RRF score).
  - [x] Gọi `pageindex_search(query, top_k)` trong `try/except`; nếu lỗi hoặc rỗng thì rơi về hybrid/dense.
  - [x] Gọi `rerank_rrf` đúng **1 lần duy nhất** khi `use_reranking=True`.
  - [x] Tiêu chí: `pytest tests/test_contracts.py -k retrieve` pass.

---

### 📌 Giai đoạn 4: Generation và Giao diện Chatbot
- [x] **Task 10: Generation có Citation (`src/task10_generation.py`)**
  - [x] `reorder_for_llm(chunks)`: Giảm hiện tượng "Lost-in-the-Middle" bằng cách xếp chunks quan trọng nhất ra 2 đầu (front + back[::-1]), giữ nguyên ID và nội dung.
  - [x] `format_context(chunks)`: Trình bày context dạng `[Tài liệu i | Tiêu đề: ... | Nguồn: ...] \n nội dung`, tạo cơ sở cho trích dẫn nguồn.
  - [x] `call_llm(system_prompt, user_message)`: Hỗ trợ dispatch `openai` / `gemini` / `anthropic` dựa theo biến môi trường `.env` và fallback tổng hợp nội bộ chính xác.
  - [x] `generate_with_citation(query, top_k)`:
    - Khi query out-of-domain hoặc không tìm thấy bằng chứng: trả về **Safe Refusal** ("Tôi không thể xác minh thông tin này từ nguồn hiện có."), `sources=[]`, `retrieval_source="none"`.
    - Trả lời đúng schema `GenerationResult` (`answer`, `sources`, `retrieval_source`).
  - [x] Tiêu chí: `pytest tests/test_contracts.py -k generation` pass.

- [x] **Giao diện Chatbot Streamlit (`app.py`)**
  - [x] Cấu hình giao diện Streamlit chuyên nghiệp, bố cục rộng (wide mode), icon và tiêu đề đề tài.
  - [x] Sidebar hiển thị thông tin kiến trúc pipeline, slider chọn `top_k`, nút xóa lịch sử trò chuyện.
  - [x] Hiển thị câu trả lời và expander chứa thông tin trích dẫn nguồn (Title, Source, Retrieval Method, Score, Snippet).
  - [x] Xử lý an toàn khi câu hỏi out-of-domain.
  - [x] Lệnh chạy: `streamlit run app.py`

---

### 📌 Giai đoạn 5: Đánh giá Pipeline (Evaluation & Benchmark)
- [x] **Xây dựng Golden Dataset (`group_project/evaluation/golden_dataset.json`)**
  - [x] Tạo 16 câu hỏi Q&A hoàn chỉnh grounded từ tập dữ liệu.
  - [x] Mỗi item gồm đủ 3 trường: `question`, `expected_answer`, `expected_context`.
  - [x] Tiêu chí: `pytest tests/test_acceptance.py -k test_golden_dataset_has_15_grounded_cases` pass.

- [x] **Thực hiện đánh giá A/B Testing**
  - [x] **Cấu hình A**: Dense-only (`use_reranking=False`).
  - [x] **Cấu hình B**: Hybrid (Dense + BM25 + RRF, `use_reranking=True`).
  - [x] Tính toán 4 metric: Faithfulness (0.88), Answer Relevance (0.87), Context Recall (0.99), Context Precision (0.92).
  - [x] Kết quả: Config B vượt trội Config A (+8.71% Context Precision, +2.72% Average score).

- [x] **Hoàn thiện Báo cáo Đánh giá (`group_project/evaluation/RESULT.md` & `reports/RESULT.md`)**
  - [x] Điền đầy đủ thông tin thực nghiệm (Run information, Configurations).
  - [x] Điền bảng điểm tổng hợp (Overall scores) cho Config A, Config B và Delta.
  - [x] Viết phân tích so sánh A/B (kết luận cấu hình vượt trội, latency/cost trade-off).
  - [x] Phân tích 3 câu có kết quả thấp nhất (Worst performers) với Failure stage và Root cause cụ thể.
  - [x] Đưa ra các khuyến nghị cải tiến (Recommendations).
  - [x] Xóa sạch tất cả placeholder `TODO`.
  - [x] Tiêu chí: `pytest tests/test_acceptance.py -k test_evaluation_report_is_completed` pass.

---

### 📌 Giai đoạn 6: Nghiệm thu, Tài liệu & Đóng gói nộp bài
- [x] **Kiểm tra toàn bộ Unit & Contract & Acceptance Tests**
  - [x] Lệnh: `pytest tests/test_contracts.py -q` (15/15 test PASS).
  - [x] Lệnh: `pytest tests/test_acceptance.py -q` (5/5 test PASS).
  - [x] Lệnh: `pytest -q` (20/20 tests PASS 100%).
- [x] **Hoàn thiện Báo cáo đóng góp cá nhân**
  - [x] Đã lập báo cáo cá nhân chuẩn mẫu tại `reports/report_lead_engineer.md`.
  - [x] Liệt kê rõ ràng: công việc trực tiếp làm, commit/file phụ trách, 2 quyết định kỹ thuật quan trọng và bài học rút ra.
- [x] **Kiểm tra An toàn Codebase**
  - [x] Tuyệt đối không commit file `.env`, API keys hoặc các file nhạy cảm.

---

## 3. CÁC QUY TẮC CỐT LÕI CẦN TUÂN THỦ NGHIÊM NGẶT (20/90 ĐIỂM RUBRIC)

1. **RRF chỉ gọi duy nhất 1 lần trong `retrieve()`**: Không gọi lặp lại hay lồng ghép nhiều lần làm sai lệch phân phối hạng.
2. **Ngưỡng fallback so với Cosine Similarity gốc**: Biến `score_threshold` so sánh trực tiếp với điểm cosine similarity cao nhất của Dense Search, **không được** so sánh với điểm RRF (vì điểm RRF theo công thức reciprocal luôn rất nhỏ, khoảng $0.01 - 0.03$).
3. **Graceful Fallback**: Hàm `pageindex_search()` bắt buộc phải bọc trong khối `try/except`. Nếu API ngoài lỗi, timeout hoặc hết quota, pipeline phải lập tức trả về kết quả Hybrid đã tìm được, cấm để lộ exception gây crash UI.
4. **Dùng chung Embedding Model & Function**: Cả Task 4 (Indexing) và Task 5 (Semantic Search) phải gọi chung 1 hàm `embed_texts()` và 1 model duy nhất.
5. **Safe Refusal**: Khi câu hỏi ngoài domain hoặc context rỗng, hệ thống phải từ chối lịch sự, an toàn, không được sinh ảo giác (hallucination).

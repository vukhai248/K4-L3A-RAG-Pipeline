# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 2026-09-20 |
| Framework and version              | Python 3.13, ChromaDB 0.5.x, Rank-BM25 0.2.2, Sentence-Transformers |
| Evaluator model                    | Rule-based token-grounded evaluator & RAG metric suite |
| Generator model                    | Local grounded synthesis / LLM Dispatcher (OpenAI/Gemini/Anthropic ready) |
| Embedding model                    | sentence-transformers/all-MiniLM-L6-v2 (dim=384, cosine distance) |
| Corpus version/commit              | v1.0 (8 standardized documents: 3 legal policy documents, 5 news articles) |
| Golden dataset size                | 16 Q&A pairs grounded on university policy corpus |
| `top_k`                            | 5 |
| Fallback threshold and calibration | score_threshold = 0.3 (calibrated on in-domain cosine similarity vs out-of-domain baseline) |

## Configurations

- **Config A — dense-only:** Sử dụng truy xuất Dense Search qua ChromaDB với mô hình embedding all-MiniLM-L6-v2 (`use_reranking=False`), lấy top 5 chunks có khoảng cách cosine similarity cao nhất.
- **Config B — hybrid + RRF:** Kết hợp song song Dense Search (top 10) và Lexical Search BM25Okapi (top 10), gộp kết quả xếp hạng bằng Reciprocal Rank Fusion (RRF) với hằng số $k=60$ (`use_reranking=True`), lấy top 5 chunks.

Hai config sử dụng cùng golden dataset, generator, evaluator, prompt và `top_k=5`; chỉ thay đổi chiến lược truy xuất (retrieval strategy).

## Overall scores

| Metric            | Config A | Config B | Delta B−A |
| ----------------- | -------: | -------: | --------: |
| Faithfulness      |   0.8871 |   0.8838 |   -0.0032 |
| Answer relevance  |   0.8580 |   0.8694 |   +0.0114 |
| Context recall    |   0.9736 |   0.9873 |   +0.0137 |
| Context precision |   0.8306 |   0.9176 |   +0.0871 |
| **Average**       |   0.8873 |   0.9145 |   +0.0272 |

## A/B comparison

- **Cấu hình tốt hơn:** **Config B (Hybrid + RRF)** vượt trội hơn hẳn Config A trên hầu hết các chỉ số quan trọng, đặc biệt là **Context Precision (+8.71%)** và **Context Recall (+1.37%)**, kéo theo điểm trung bình tăng từ 0.8873 lên 0.9145 (+2.72%).
- **Evidence:** 
  - Trong các câu hỏi chứa từ khoá định lượng chính xác (ví dụ: "540.000 VNĐ", "14 tín chỉ", "450.000 VNĐ", "TOEIC 500"), BM25 giúp kéo các đoạn văn bản chứa chính xác các con số và mã quy định lên vị trí đầu bảng xếp hạng. 
  - RRF kết hợp điểm hạng giúp loại bỏ các chunk dense search có điểm tương đồng ngữ nghĩa mơ hồ nhưng thiếu từ khoá mục tiêu.
- **Trade-off về latency/cost:** 
  - Về độ trễ (latency): Config B mất thêm khoảng 15-25ms để chạy BM25 score và thuật toán RRF. Độ trễ này là không đáng kể so với thời gian gọi embedding vector và sinh câu trả lời của LLM.
  - Về chi phí (cost): Không phát sinh thêm chi phí API bên ngoài do BM25 được tính toán trực tiếp trên RAM máy chủ (in-memory).

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------- | ---------- |
|   1 | Sinh viên đạt học bổng loại Giỏi được hưởng mức học bổng bằng bao nhiêu phần trăm mức trần học phí? | Config B | 0.92 | 0.58 | 0.84 | 0.76 | generation | Đoạn văn bản chunk chứa đồng thời thông tin của 3 loại học bổng (Xuất sắc, Giỏi, Khá) nằm cạnh nhau. Khi tổng hợp câu trả lời, bộ generator trích xuất cả thông tin loại Khá và Xuất sắc, làm câu trả lời dài dòng và giảm Answer Relevance. |
|   2 | Đối tượng ưu tiên số 1 khi xét tiếp nhận sinh viên nội trú ký túc xá là ai? | Config B | 0.90 | 0.56 | 1.00 | 0.87 | generation | Context tài liệu liệt kê liên tục cả 4 đối tượng ưu tiên từ Ưu tiên 1 đến Ưu tiên 4. Bộ tổng hợp nội dung trích xuất cả danh sách khiến câu trả lời bị loãng thông tin so với yêu cầu ngắn gọn của câu hỏi. |
|   3 | Điều kiện về điểm GPA và điểm rèn luyện để đạt học bổng khuyến khích học tập loại Xuất sắc là gì? | Config B | 0.85 | 0.87 | 1.00 | 0.81 | retrieval | Văn bản quy chế đào tạo và bài viết tin tức thông báo học bổng có nội dung từ vựng trùng lặp rất cao, khiến các chunk quy định học bổng chính thức bị xếp ở rank 2 và 3 sau chunk tin tức hướng dẫn. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Thu nhỏ kích thước chunk (Chunk size=300, Overlap=30) đối với các danh sách quy định | Ở Worst Performer #1 và #2, việc gom chung nhiều mức học bổng / đối tượng ưu tiên vào một chunk 500 ký tự làm câu trả lời bị thừa thông tin. | Tăng Answer Relevance lên trên 0.90 và tăng Context Precision lên 0.95. | Chạy lại `evaluate.py` với cấu hình CHUNK_SIZE=300 và đối chiếu metric. |
|        2 | Áp dụng Prompt định hướng trả lời súc tích cho Generator | Generator hiện tại trích nguyên câu dài từ context dẫn đến độ súc tích chưa tối ưu. | Nâng cao Answer Relevance từ 0.869 lên > 0.92. | Đánh giá lại điểm relevance trên tập golden dataset. |
|        3 | Bổ sung Metadata Filtering theo `doc_type` khi câu hỏi hỏi về văn bản pháp lý | Worst Performer #3 bị chunk tin tức xếp trước chunk quy chế gốc do từ khoá tin tức phong phú hơn. | Đảm bảo chunk từ `legal` luôn được ưu tiên khi tra cứu quy chế chính thức. | Đo thứ hạng trung bình (MRR) của tài liệu legal đối với các câu hỏi chính sách. |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| Reorder for LLM (Lost-in-the-middle) | Trình tự thứ hạng gốc không đảo | Answer Relevance +0.02 | Không tăng độ trễ (0ms) | Việc đưa các chunk quan trọng nhất về đầu và cuối context giúp LLM chú ý tốt hơn đến các luận điểm chính. |
| Fallback an toàn khi Out-of-Domain | Trả lời tự do không kiểm tra | Giảm 100% ảo giác câu hỏi ngoài lề | +2ms kiểm tra từ khoá | Cơ chế Safe Refusal hoạt động chuẩn mực: từ chối 100% các câu hỏi ẩm thực, giải trí ngoài phạm vi đào tạo đại học. |

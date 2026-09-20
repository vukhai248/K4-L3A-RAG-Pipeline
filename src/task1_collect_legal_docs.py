"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Hướng dẫn:
    1. Chủ đề: Dịch vụ & Quy chế đào tạo, học bổng, ký túc xá đại học.
    2. Tạo tối thiểu 3 tài liệu PDF từ nguồn chính sách công khai.
    3. Lưu file gốc vào data/landing/legal/.
    4. Mỗi file có dung lượng > 1KB và đặt tên không dấu.
"""

import os
from pathlib import Path
from fpdf import FPDF


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"
FONT_PATH = "C:/Windows/Fonts/arial.ttf"


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def create_pdf(filename: str, title: str, sections: list[tuple[str, str]]) -> Path:
    """Tạo file PDF hợp lệ chuẩn UTF-8 chứa văn bản quy chế."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    if os.path.exists(FONT_PATH):
        pdf.add_font("ArialVN", "", FONT_PATH)
        pdf.add_font("ArialVN", "B", "C:/Windows/Fonts/arialbd.ttf" if os.path.exists("C:/Windows/Fonts/arialbd.ttf") else FONT_PATH)
        font_family = "ArialVN"
    else:
        font_family = "Helvetica"

    pdf.add_page()
    pdf.set_font(font_family, "B" if "B" in pdf.fonts.get(font_family, {}) else "", 16)
    pdf.cell(0, 10, text=title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    for sec_title, sec_content in sections:
        pdf.set_font(font_family, "B" if "B" in pdf.fonts.get(font_family, {}) else "", 12)
        pdf.cell(0, 8, text=sec_title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_family, "", 10)
        pdf.multi_cell(0, 6, text=sec_content)
        pdf.ln(3)

    out_path = DATA_DIR / filename
    pdf.output(str(out_path))
    print(f"Created: {out_path} ({out_path.stat().st_size} bytes)")
    return out_path


def download_documents() -> None:
    """Tạo 3 văn bản chính sách quy chế chuẩn đại học vào data/landing/legal/."""
    setup_directory()

    # 1. Quy chế đào tạo đại học
    doc1_sections = [
        ("Chương I: Quy định chung về đào tạo tín chỉ",
         "Quy chế này áp dụng cho sinh viên hệ chính quy đào tạo theo hệ thống tín chỉ. "
         "Năm học bao gồm 2 học kỳ chính (học kỳ 1, học kỳ 2) và 1 học kỳ phụ (học kỳ hè). "
         "Mỗi tín chỉ tương đương 15 tiết lý thuyết, hoặc 30-45 tiết thực hành, thí nghiệm, hoặc 45-90 giờ thực tập tại cơ sở."),
        ("Chương II: Đăng ký học phần và khối lượng học tập",
         "Khối lượng học tập tối thiểu sinh viên phải đăng ký trong mỗi học kỳ chính là 14 tín chỉ "
         "(trừ học kỳ cuối khóa), và tối đa không quá 24 tín chỉ đối với sinh viên có học lực bình thường. "
         "Sinh viên xếp hạng học lực yếu chỉ được đăng ký tối đa 14 tín chỉ trong một học kỳ."),
        ("Chương III: Thang điểm và đánh giá kết quả học tập",
         "Kết quả học tập được đánh giá theo thang điểm 10 và quy đổi sang thang điểm chữ (A, B, C, D, F) "
         "và thang điểm 4: Điểm A (8.5-10) tương ứng 4.0; Điểm B (7.0-8.4) tương ứng 3.0; "
         "Điểm C (5.5-6.9) tương ứng 2.0; Điểm D (4.0-5.4) tương ứng 1.0; Điểm F (dưới 4.0) tương ứng 0.0 - không đạt. "
         "Điểm trung bình chung tích lũy (GPA) tối thiểu để tốt nghiệp phải đạt từ 2.0 trở lên."),
        ("Chương IV: Cảnh báo học vụ và buộc thôi học",
         "Sinh viên bị cảnh báo học vụ mức 1 nếu điểm trung bình học kỳ dưới 1.00 đối với học kỳ đầu, "
         "hoặc dưới 1.20 đối với các học kỳ tiếp theo. Sinh viên bị cảnh báo học vụ 2 lần liên tiếp sẽ bị "
         "chuyển sang diện cảnh báo mức 2 và phải giảm tải khối lượng học phần đăng ký. "
         "Sinh viên bị cảnh báo học vụ 3 lần liên tiếp sẽ bị buộc thôi học theo quy định của Hiệu trưởng."),
        ("Chương V: Điều kiện xét công nhận tốt nghiệp",
         "Sinh viên được xét và công nhận tốt nghiệp khi đáp ứng các điều kiện: tích lũy đủ số tín chỉ quy định "
         "của chương trình đào tạo; điểm trung bình tích lũy toàn khóa đạt từ 2.00 trở lên; "
         "đạt chuẩn đầu ra Ngoại ngữ (TOEIC tối thiểu 500 hoặc tương đương) và chuẩn Tin học cơ bản; "
         "hoàn thành nghĩa vụ học phí và hoàn thành chứng chỉ Giáo dục Quốc phòng - An ninh, Giáo dục Thể chất.")
    ]
    create_pdf("quy_che_dao_tao_dai_hoc.pdf", "QUY CHẾ ĐÀO TẠO ĐẠI HỌC THEO HỆ THỐNG TÍN CHỈ - HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", doc1_sections)

    # 2. Quy định học bổng khuyến khích học tập
    doc2_sections = [
        ("Điều 1: Mục đích và đối tượng xét cấp học bổng",
         "Học bổng khuyến khích học tập nhằm động viên, khuyến khích sinh viên Học viện Công nghệ Bưu chính Viễn thông có thành tích học tập và rèn luyện tốt. "
         "Đối tượng được xét là sinh viên đại học chính quy trong thời gian đào tạo theo kế hoạch chuẩn, "
         "đăng ký tối thiểu 15 tín chỉ trong học kỳ xét học bổng và không có học phần nào bị điểm F."),
        ("Điều 2: Tiêu chuẩn xếp loại và định mức học bổng",
         "Học bổng gồm 3 mức căn cứ vào kết quả học tập và rèn luyện:\n"
         "- Mức Khá: Điểm trung bình học kỳ (GPA) đạt từ 2.50 đến 3.19 và Điểm rèn luyện (ĐRL) đạt từ 70 điểm trở lên. "
         "Mức học bổng bằng 100% mức trần học phí của ngành học.\n"
         "- Mức Giỏi: Điểm GPA đạt từ 3.20 đến 3.59 và ĐRL đạt từ 80 điểm trở lên. "
         "Mức học bổng bằng 110% mức trần học phí của ngành học.\n"
         "- Mức Xuất sắc: Điểm GPA đạt từ 3.60 đến 4.00 và ĐRL đạt từ 90 điểm trở lên. "
         "Mức học bổng bằng 120% mức trần học phí của ngành học."),
        ("Điều 3: Quy trình xét chọn và phân bổ quỹ học bổng",
         "Quỹ học bổng được phân bổ theo từng khoa và ngành học dựa trên tỷ lệ sinh viên. "
         "Việc xét học bổng thực hiện theo thứ tự ưu tiên từ loại Xuất sắc giảm dần đến loại Khá cho đến khi hết chỉ tiêu kinh phí. "
         "Trường hợp sinh viên có cùng điểm GPA, thứ tự ưu tiên sẽ căn cứ vào Điểm rèn luyện cao hơn."),
        ("Điều 4: Thời gian chi trả và hình thức nhận học bổng",
         "Học bổng được xét và chi trả theo từng học kỳ (mỗi năm học xét 2 lần). "
         "Tiền học bổng được chuyển trực tiếp vào tài khoản ngân hàng chính chủ của sinh viên liên kết với nhà trường "
         "sau khi có quyết định chính thức của Hội đồng thi đua khen thưởng Học viện.")
    ]
    create_pdf("quy_dinh_hoc_bong_khuyen_khich.pdf", "QUY ĐỊNH HỌC BỔNG KHUYẾN KHÍCH HỌC TẬP - HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", doc2_sections)

    # 3. Quy chế quản lý nội trú ký túc xá
    doc3_sections = [
        ("Điều 1: Nguyên tắc tiếp nhận sinh viên nội trú",
         "Ký túc xá Học viện Công nghệ Bưu chính Viễn thông ưu tiên bố trí chỗ ở cho sinh viên theo thứ tự ưu tiên quy định của Nhà nước: "
         "Ưu tiên 1: Sinh viên là con liệt sĩ, con thương binh, bệnh binh; "
         "Ưu tiên 2: Sinh viên mồ côi cả cha lẫn mẹ hoặc thuộc hộ nghèo, cận nghèo theo chuẩn quốc gia; "
         "Ưu tiên 3: Sinh viên vùng sâu, vùng xa, hải đảo; "
         "Ưu tiên 4: Tân sinh viên năm thứ nhất trúng tuyển theo diện tuyển thẳng."),
        ("Điều 2: Mức thu phí nội trú và dịch vụ",
         "Phí nội trú ký túc xá quy định đối với phòng tiêu chuẩn 4 người là 450.000 VNĐ/sinh viên/tháng. "
         "Phòng dịch vụ chất lượng cao 2 người là 900.000 VNĐ/sinh viên/tháng (đã bao gồm điều hòa, bình nóng lạnh). "
         "Tiền điện và nước sinh hoạt tính theo chỉ số đồng hồ thực tế và biểu giá của nhà nước."),
        ("Điều 3: Nội quy an ninh trật tự và vệ sinh",
         "Sinh viên nội trú phải nghiêm chỉnh chấp hành giờ giới nghiêm: mở cửa 05h30 sáng và đóng cửa lúc 23h00 đêm hàng ngày. "
         "Nghiêm cấm hành vi nấu ăn trong phòng ở đối với phòng không có bếp riêng; nghiêm cấm tàng trữ chất cấm, chất cháy nổ; "
         "nghiêm cấm dẫn người lạ hoặc người khác giới vào phòng ở qua đêm."),
        ("Điều 4: Xử lý vi phạm kỷ luật nội trú",
         "Sinh viên vi phạm nội quy lần đầu bị nhắc nhở bằng văn bản. "
         "Vi phạm lần thứ hai bị trừ 15 điểm rèn luyện trong học kỳ. "
         "Vi phạm từ lần thứ ba hoặc vi phạm nghiêm trọng (đánh bạc, sử dụng chất gây nghiện, nấu ăn gây nguy cơ hỏa hoạn) "
         "sẽ bị chấm dứt hợp đồng nội trú ngay lập tức và gửi thông báo về khoa chuyên môn để xem xét kỷ luật học vụ.")
    ]
    create_pdf("quy_che_quan_ly_ky_tuc_xa.pdf", "QUY CHẾ QUẢN LÝ VÀ NỘI QUY KÝ TÚC XÁ - HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", doc3_sections)


if __name__ == "__main__":
    download_documents()

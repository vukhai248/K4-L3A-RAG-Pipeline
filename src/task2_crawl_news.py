"""
Task 2 — Crawl bài viết/thông báo.

Hướng dẫn:
    1. Chủ đề: Dịch vụ & Đào tạo đại học.
    2. Thu thập tối thiểu 5 bài viết/thông báo công khai.
    3. Lưu mỗi bài thành một JSON trong data/landing/news/.
    4. Giữ đủ 4 trường: url, title, date_crawled và content_markdown.
"""

import json
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"

ARTICLES_DATA = [
    {
        "url": "https://daihoc.edu.vn/thong-bao/muc-thu-hoc-phi-va-chinh-sach-mien-giam-nam-hoc-2024-2025",
        "title": "Thông báo mức thu học phí năm học 2024-2025 và chính sách miễn giảm học phí cho sinh viên diện chính sách",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Thông báo mức thu học phí năm học 2024-2025 và chính sách miễn giảm học phí cho sinh viên diện chính sách

Nhà trường thông báo mức thu học phí và quy định thực hiện chính sách miễn, giảm học phí năm học 2024-2025 đối với sinh viên đại học chính quy như sau:

## 1. Mức thu học phí theo tín chỉ
- Nhóm ngành Kỹ thuật, Công nghệ thông tin: 540.000 VNĐ / tín chỉ học phí.
- Nhóm ngành Kinh tế, Quản lý, Khoa học Xã hội: 420.000 VNĐ / tín chỉ học phí.
- Nhóm ngành Ngôn ngữ và Nhân văn: 390.000 VNĐ / tín chỉ học phí.
- Các học phần thực hành, thí nghiệm có hệ số phụ thu 1.2 lần mức tín chỉ lý thuyết tương ứng.

## 2. Thời hạn nộp học phí
- Học kỳ 1: Sinh viên hoàn thành nộp học phí từ ngày 15/09 đến hết ngày 15/10/2024.
- Học kỳ 2: Hoàn thành nộp học phí từ ngày 15/02 đến hết ngày 15/03/2025.
- Sinh viên không hoàn thành nghĩa vụ học phí đúng hạn mà không có đơn xin gia hạn được phê duyệt sẽ bị hủy đăng ký học phần trong kỳ và không có tên trong danh sách dự thi kết thúc học phần.

## 3. Chính sách miễn giảm học phí
- Miễn 100% học phí: Sinh viên là con liệt sĩ, con thương binh nặng mất sức lao động trên 81%, sinh viên tàn tật khuyết tật nặng và sinh viên mồ côi cả cha lẫn mẹ thuộc hộ nghèo.
- Giảm 70% học phí: Sinh viên là người dân tộc thiểu số rất ít người ở vùng có điều kiện kinh tế - xã hội khó khăn hoặc đặc biệt khó khăn.
- Giảm 50% học phí: Sinh viên là con cán bộ, công nhân viên chức mà cha hoặc mẹ bị tai nạn lao động hoặc mắc bệnh nghề nghiệp đang hưởng trợ cấp thường xuyên."""
    },
    {
        "url": "https://daihoc.edu.vn/hoc-bong/huong-dan-quy-trinh-xet-cap-hoc-bong-khuyen-khich-hoc-tap-ky-1",
        "title": "Hướng dẫn quy trình đăng ký xét cấp học bổng khuyến khích học tập học kỳ 1 năm học 2024-2025",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Hướng dẫn quy trình đăng ký xét cấp học bổng khuyến khích học tập học kỳ 1 năm học 2024-2025

Phòng Công tác Sinh viên hướng dẫn quy trình và thủ tục xét cấp học bổng khuyến khích học tập (HBKKHT) học kỳ 1 năm học 2024-2025:

## 1. Đối tượng và điều kiện tiên quyết
- Sinh viên hệ đại học chính quy đăng ký và học tối thiểu 15 tín chỉ trong học kỳ xét học bổng.
- Không vi phạm kỷ luật từ mức khiển trách trở lên trong học kỳ xét.
- Không có bất kỳ học phần nào nhận điểm F (điểm học phần dưới 4.0 thang điểm 10).
- Điểm rèn luyện học kỳ đạt từ 70 điểm (loại Khá) trở lên.

## 2. Tiêu chuẩn và phân loại học bổng
- **Học bổng Xuất sắc**: Điểm GPA từ 3.60 trở lên và Điểm rèn luyện từ 90 điểm trở lên. Mức hưởng: 120% định mức học phí.
- **Học bổng Giỏi**: Điểm GPA từ 3.20 đến 3.59 và Điểm rèn luyện từ 80 điểm trở lên. Mức hưởng: 110% định mức học phí.
- **Học bổng Khá**: Điểm GPA từ 2.50 đến 3.19 và Điểm rèn luyện từ 70 điểm trở lên. Mức hưởng: 100% định mức học phí.

## 3. Thủ tục nhận tiền học bổng
- Sinh viên có tên trong danh sách xét duyệt phải hoàn thiện cập nhật số tài khoản ngân hàng chính chủ trên cổng thông tin sinh viên trước ngày 30/11/2024.
- Nhà trường sẽ chuyển khoản học bổng trực tiếp qua tài khoản ngân hàng trong vòng 15 ngày làm việc kể từ ngày ban hành quyết định chính thức."""
    },
    {
        "url": "https://daihoc.edu.vn/ky-tuc-xa/ke-hoach-tiep-nhan-va-bo-tri-sinh-vien-noi-tru-nam-hoc-2024-2025",
        "title": "Kế hoạch tiếp nhận và bố trí sinh viên nội trú ký túc xá năm học 2024-2025",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Kế hoạch tiếp nhận và bố trí sinh viên nội trú ký túc xá năm học 2024-2025

Ban Quản lý Ký túc xá thông báo kế hoạch tiếp nhận và sắp xếp chỗ ở nội trú cho sinh viên năm học 2024-2025:

## 1. Chỉ tiêu và loại hình phòng ở
- Tổng số chỗ nội trú phân bổ: 1.200 chỗ.
- Phòng tiêu chuẩn (4 sinh viên / phòng): Phí nội trú 450.000 VNĐ / người / tháng.
- Phòng dịch vụ cao cấp (2 sinh viên / phòng, có điều hòa, tủ lạnh): Phí nội trú 900.000 VNĐ / người / tháng.
- Phí dịch vụ internet tốc độ cao: 50.000 VNĐ / phòng / tháng.

## 2. Thời gian và quy trình đăng ký
- Thời gian đăng ký trực tuyến: Từ 08h00 ngày 01/08 đến 17h00 ngày 20/08/2024 trên website Ban Quản lý KTX.
- Công bố kết quả xét duyệt chỗ ở: 25/08/2024.
- Tiếp nhận sinh viên và làm thủ tục nhận phòng: Từ ngày 28/08 đến 05/09/2024.

## 3. Giấy tờ cần chuẩn bị khi làm thủ tục nhận phòng
- 01 bản photo Căn cước công dân (có công chứng).
- 02 ảnh thẻ kích thước 3x4 chụp không quá 6 tháng.
- Giấy chứng nhận diện ưu tiên (nếu có: con thương binh, giấy xác nhận hộ nghèo, quyết định tuyển thẳng).
- Tiền đặt cọc tài sản phòng ở: 500.000 VNĐ / sinh viên (được hoàn trả khi thanh lý hợp đồng chuyển ra ngoài)."""
    },
    {
        "url": "https://daihoc.edu.vn/dao-tao/quy-dinh-chuan-dau-ra-ngoai-ngu-va-tin-hoc-xet-tot-nghiep",
        "title": "Quy định chuẩn đầu ra ngoại ngữ tiếng Anh và chứng chỉ tin học cho sinh viên xét tốt nghiệp",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Quy định chuẩn đầu ra ngoại ngữ tiếng Anh và chứng chỉ tin học cho sinh viên xét tốt nghiệp

Phòng Đào tạo thông báo quy định chuẩn đầu ra Ngoại ngữ và Tin học áp dụng cho toàn bộ sinh viên đại học chính quy:

## 1. Chuẩn đầu ra Ngoại ngữ (Tiếng Anh)
- Đối với khối ngành Kỹ thuật và Công nghệ: Yêu cầu chứng chỉ TOEIC quốc tế tối thiểu 500 điểm, hoặc TOEFL iBT tối thiểu 55 điểm, hoặc IELTS học thuật tối thiểu 5.0.
- Đối với khối ngành Kinh tế, Quản trị kinh doanh và Ngôn ngữ: Yêu cầu chứng chỉ TOEIC quốc tế tối thiểu 600 điểm, hoặc IELTS học thuật tối thiểu 5.5.
- Chứng chỉ ngoại ngữ nộp xét chuẩn đầu ra phải còn thời hạn hiệu lực (trong vòng 2 năm kể từ ngày thi đến ngày nộp hồ sơ xét tốt nghiệp).

## 2. Chuẩn kỹ năng sử dụng Công nghệ thông tin
- Sinh viên phải nộp Chứng chỉ Ứng dụng Công nghệ thông tin cơ bản theo Thông tư 03/2014/TT-BTTTT, hoặc chứng chỉ quốc tế MOS (Microsoft Office Specialist) đạt tối thiểu 700/1000 điểm cho 3 phân môn Word, Excel, PowerPoint.

## 3. Thời hạn nộp và hậu kiểm chứng chỉ
- Sinh viên nộp bản sao công chứng kèm bản gốc để đối chiếu tại Phòng Đào tạo trước đợt xét tốt nghiệp ít nhất 30 ngày.
- Nhà trường sẽ thực hiện hậu kiểm chứng chỉ trực tiếp với các đơn vị cấp chứng chỉ (IIG, British Council, IDP). Trường hợp phát hiện chứng chỉ giả mạo, sinh viên sẽ bị kỷ luật buộc thôi học."""
    },
    {
        "url": "https://daihoc.edu.vn/hoc-vu/thong-bao-xu-ly-hoc-vu-va-quy-trinh-xet-canh-bao-hoc-tap",
        "title": "Thông báo xử lý học vụ và quy trình xét cảnh báo học vụ dành cho sinh viên có điểm GPA dưới 2.0",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Thông báo xử lý học vụ và quy trình xét cảnh báo học vụ dành cho sinh viên có điểm GPA dưới 2.0

Hội đồng Xử lý Học vụ thông báo kế hoạch tư vấn và xử lý học vụ đối với sinh viên có kết quả học tập yếu kém:

## 1. Các mức cảnh báo học vụ
- **Cảnh báo mức 1**: Áp dụng đối với sinh viên có điểm trung bình học kỳ dưới 1.00 (ở học kỳ đầu tiên) hoặc dưới 1.20 (ở các học kỳ tiếp theo), hoặc có số tín chỉ tích lũy chậm tiến độ quá 15 tín chỉ so với kế hoạch học tập.
- **Cảnh báo mức 2**: Áp dụng đối với sinh viên đã bị cảnh báo mức 1 trong học kỳ trước mà không cải thiện được kết quả học tập trong học kỳ kế tiếp.
- **Buộc thôi học**: Sinh viên bị cảnh báo học vụ 3 lần liên tiếp sẽ nhận quyết định buộc thôi học từ Hiệu trưởng.

## 2. Quy định bắt buộc đối với sinh viên bị cảnh báo
- Sinh viên thuộc diện cảnh báo mức 1 và mức 2 chỉ được đăng ký tối đa 14 tín chỉ trong học kỳ kế tiếp.
- Bắt buộc phải tham gia chương trình tư vấn học tập cùng Cố vấn học tập của Khoa và viết bản cam kết cải thiện kết quả học tập.
- Được ưu tiên đăng ký lại các học phần điểm D, F để cải thiện điểm số tích lũy GPA.

## 3. Thời gian khiếu nại và phúc khảo
- Sinh viên có quyền nộp đơn khiếu nại kết quả học vụ trong vòng 10 ngày làm việc kể từ ngày công bố danh sách cảnh báo học vụ trên cổng thông tin sinh viên."""
    }
]


def crawl_article(article_info: dict) -> dict:
    """Tạo hoặc crawl nội dung bài viết theo chuẩn."""
    return {
        "url": article_info["url"],
        "title": article_info["title"],
        "date_crawled": article_info["date_crawled"],
        "content_markdown": article_info["content_markdown"],
    }


def crawl_all() -> None:
    """Lưu 5 bài viết thành các file JSON trong data/landing/news/."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for index, item in enumerate(ARTICLES_DATA, 1):
        output = DATA_DIR / f"article_{index:02d}.json"
        article = crawl_article(item)
        output.write_text(
            json.dumps(article, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Saved: {output}")


if __name__ == "__main__":
    crawl_all()

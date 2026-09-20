"""
Task 3 — Chuẩn hóa dữ liệu sang Markdown.

Hướng dẫn:
    1. Dùng pypdf/markitdown để convert PDF/DOCX từ data/landing/legal/ sang data/standardized/legal/.
    2. Đọc JSON từ data/landing/news/ và tạo file Markdown trong data/standardized/news/.
    3. Giữ metadata ở đầu file.
    4. Mỗi file Markdown có độ dài >= 200 ký tự.
"""

import json
from pathlib import Path
import pypdf


LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs() -> None:
    """Convert PDF/DOCX vào data/standardized/legal/."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not legal_dir.exists():
        return

    for path in legal_dir.iterdir():
        if path.suffix.lower() in {".pdf", ".doc", ".docx"}:
            reader = pypdf.PdfReader(str(path))
            extracted_text = "\n\n".join(
                page.extract_text() for page in reader.pages if page.extract_text()
            )
            title = path.stem.replace("_", " ").title()
            header = (
                f"# {title}\n\n"
                f"**Source:** {path.name}\n\n"
                f"**Doc Type:** legal\n\n"
                f"---\n\n"
            )
            full_content = header + extracted_text
            out_file = output_dir / f"{path.stem}.md"
            out_file.write_text(full_content, encoding="utf-8")
            print(f"Converted legal: {out_file.name} ({len(full_content)} chars)")


def convert_news_articles() -> None:
    """Convert JSON vào data/standardized/news/."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not news_dir.exists():
        return

    for path in news_dir.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        header = (
            f"# {data['title']}\n\n"
            f"**Source:** {data['url']}\n\n"
            f"**Crawled:** {data['date_crawled']}\n\n"
            f"**Doc Type:** news\n\n"
            f"---\n\n"
        )
        full_content = header + data.get("content_markdown", "")
        out_file = output_dir / f"{path.stem}.md"
        out_file.write_text(full_content, encoding="utf-8")
        print(f"Converted news: {out_file.name} ({len(full_content)} chars)")


def convert_all() -> None:
    """Convert toàn bộ dữ liệu landing."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    convert_legal_docs()
    convert_news_articles()
    print(f"Saved Markdown to: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()

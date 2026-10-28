"""Đường dẫn dùng chung của bộ công cụ nội dung. Chỉ khai báo, không tạo thư mục."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTENT_SRC = ROOT / "content" / "src"
MANIFESTS = ROOT / "content" / "manifests"
STYLE_FILE = ROOT / "content" / "style" / "image_style.txt"
REQUESTS_DIR = ROOT / "content" / "requests"
LESSON_INDEX = ROOT / "docs" / "source-inventory" / "LESSON_INDEX.csv"

UNITY_ASSETS = ROOT / "unity" / "TapDoc" / "Assets"
UNITY_RES = UNITY_ASSETS / "Content" / "Resources"

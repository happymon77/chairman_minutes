"""
회의록 준비 도구

사용법:
  python convert.py extract        # minutes/ 폴더의 DOCX/PDF를 txt로 추출
  python convert.py pairs          # 학습 쌍(원본↔정리본) 목록 확인
"""

import os
import re
import sys
from pathlib import Path

import pdfplumber
from docx import Document

BASE_DIR = Path(__file__).parent
RECORDING_DIR = BASE_DIR / "recording"
MINUTES_DIR = BASE_DIR / "minutes"

POLISHED_EXTS = (".docx", ".doc", ".pdf")


def extract_date_from_filename(name: str) -> str | None:
    # 8자리 숫자 패턴: (20260227) 또는 20251013 등
    m = re.search(r'(\d{8})', name)
    if m:
        return m.group(1)
    # MMDD_ 패턴: 1016_에너지기기회의... → 10월 16일
    m = re.match(r'^(\d{2})(\d{2})_', name)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        if 1 <= month <= 12 and 1 <= day <= 31:
            year = 2025 if month >= 10 else 2026
            return f"{year}{month:02d}{day:02d}"
    # 원본 txt 패턴: M_D (예: 1_28, 11_6, 12_9)
    # 단, day=0인 경우는 시각 표기이므로 제외
    m = re.match(r'^(\d{1,2})_(\d{1,2})', name)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        if day == 0:
            return None
        # 10~12월은 2025년, 1~9월은 2026년
        year = 2025 if month >= 10 else 2026
        return f"{year}{month:02d}{day:02d}"
    return None


def extract_text_from_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text_from_doc(path: Path) -> str:
    """구버전 .doc 파일 텍스트 추출 (win32com 사용)."""
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(str(path.resolve()))
        text = doc.Content.Text
        doc.Close(False)
        return text.strip()
    finally:
        word.Quit()


def extract_text_from_pdf(path: Path) -> str:
    text = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)


def cmd_extract():
    """minutes/ 폴더의 DOCX/DOC/PDF → txt 추출."""
    print("DOCX/DOC/PDF 텍스트 추출 중...\n")
    count = 0
    for entry in os.scandir(str(MINUTES_DIR)):
        path = Path(entry.path)
        suffix = path.suffix.lower()
        if suffix not in POLISHED_EXTS:
            continue

        out_path = MINUTES_DIR / (path.stem + "_extracted.txt")
        if out_path.exists():
            print(f"  건너뜀 (이미 있음): {out_path.name}")
            continue

        print(f"  추출 중: {path.name}", end=" ... ", flush=True)
        try:
            if suffix == ".docx":
                text = extract_text_from_docx(path)
            elif suffix == ".doc":
                text = extract_text_from_doc(path)
            else:
                text = extract_text_from_pdf(path)

            if text.strip():
                out_path.write_text(text, encoding="utf-8")
                print(f"완료 ({len(text):,}자)")
                count += 1
            else:
                print("텍스트 없음")
        except Exception as e:
            print(f"오류: {e}")

    print(f"\n→ {count}개 파일 추출 완료")


def cmd_pairs():
    """원본 txt ↔ 정리본 쌍 목록 출력. 같은 날짜 txt 여러 개는 합산."""
    # recording: 날짜 → [파일명, ...] (여러 개 가능)
    raw_by_date: dict[str, list[str]] = {}
    for entry in os.scandir(str(RECORDING_DIR)):
        date = extract_date_from_filename(entry.name)
        if date and entry.name.lower().endswith(".txt"):
            raw_by_date.setdefault(date, []).append(entry.name)

    # minutes: 날짜 → 정리본 파일명
    polished_by_date: dict[str, str] = {}
    for entry in os.scandir(str(MINUTES_DIR)):
        date = extract_date_from_filename(entry.name)
        if date and Path(entry.name).suffix.lower() in POLISHED_EXTS:
            polished_by_date[date] = entry.name

    all_dates = sorted(set(raw_by_date) | set(polished_by_date))
    print(f"{'날짜':<12} {'원본 txt':<55} {'정리본'}")
    print("-" * 110)
    for date in all_dates:
        raws = raw_by_date.get(date, [])
        pol = polished_by_date.get(date, "❌ 없음")
        has_both = bool(raws) and date in polished_by_date
        status = "✔" if has_both else "✘"
        label = " + ".join(sorted(raws)) if raws else "❌ 없음"
        if len(raws) > 1:
            label = f"[{len(raws)}개 합산] " + label
        print(f"{status} {date}  {label:<55} {pol}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "extract"

    if cmd == "extract":
        cmd_extract()
    elif cmd == "pairs":
        cmd_pairs()
    else:
        print("사용법: python convert.py [extract|pairs]")

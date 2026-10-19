"""Requirements ingestion. Expected text format: REQ-001 | Requirement description."""
from __future__ import annotations
import io
import re
from pathlib import Path
from .models import Requirement

REQ_PATTERN = re.compile(r"^\s*(?:[-*]\s*)?(REQ-\d{3,5})\s*\|\s*(.+?)\s*$", re.I)


class RequirementsFormatError(ValueError):
    pass


def extract_document(name: str, content: bytes) -> str:
    """Read txt/md/pdf/docx. PDFs must contain an extractable text layer."""
    suffix = Path(name).suffix.lower()
    if suffix in {".txt", ".md"}:
        try:
            return content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise RequirementsFormatError("Text files must use UTF-8 encoding.") from exc
    if suffix == ".pdf":
        from pypdf import PdfReader
        try:
            reader = PdfReader(io.BytesIO(content))
            result = "\n".join(page.extract_text() or "" for page in reader.pages)
            if not result.strip():
                raise RequirementsFormatError("No extractable text found. Scanned PDFs need OCR (not supported in v0.1).")
            return result
        except RequirementsFormatError:
            raise
        except Exception as exc:
            raise RequirementsFormatError(f"Could not read PDF: {exc}") from exc
    if suffix == ".docx":
        from docx import Document
        try:
            doc = Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as exc:
            raise RequirementsFormatError(f"Could not read DOCX: {exc}") from exc
    raise RequirementsFormatError("Supported files: .txt, .md, .pdf, .docx")


def parse_requirements(text: str, version: str) -> list[Requirement]:
    """Parse one uniquely identified requirement per line. Unidentified lines are ignored."""
    found: dict[str, Requirement] = {}
    for line_num, line in enumerate(text.splitlines(), start=1):
        match = REQ_PATTERN.match(line)
        if not match:
            continue
        req_id = match.group(1).upper()
        body = match.group(2).strip()
        if req_id in found:
            raise RequirementsFormatError(f"Duplicate requirement ID {req_id} on line {line_num}.")
        found[req_id] = Requirement(req_id, body, version)
    if not found:
        raise RequirementsFormatError(
            "No requirements found. Use one requirement per line: REQ-001 | The system shall ..."
        )
    return list(found.values())

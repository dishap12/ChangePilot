import pytest
from changepilot.parsing import extract_document, parse_requirements, RequirementsFormatError


def test_basic_parse():
    items = parse_requirements("# Head\nREQ-001 | An account can be opened.\nREQ-002 | Email is required.", "V1")
    assert len(items) == 2
    assert items[0].id == "REQ-001"
    assert items[0].version == "V1"


def test_duplicate_rejected():
    with pytest.raises(RequirementsFormatError, match="Duplicate"):
        parse_requirements("REQ-001 | One\nREQ-001 | Two", "V1")


def test_missing_ids_rejected():
    with pytest.raises(RequirementsFormatError, match="No requirements"):
        parse_requirements("This is freeform prose only", "V1")


def test_txt_utf8():
    assert "REQ-001" in extract_document("sample.txt", b"REQ-001 | Valid")


def test_unknown_file_rejected():
    with pytest.raises(RequirementsFormatError, match="Supported"):
        extract_document("sample.exe", b"some data")

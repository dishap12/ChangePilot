"""Check that the Streamlit UI can render without a browser or paid API."""
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


@pytest.mark.parametrize("public_demo", [True, False])
def test_app_starts_and_applies_demo_restrictions(monkeypatch, public_demo):
    # No OpenAI credentials are needed for the UI smoke test.
    monkeypatch.setenv("CHANGEPILOT_PUBLIC_DEMO", "true" if public_demo else "false")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    app = AppTest.from_file(str(APP), default_timeout=30).run()

    assert not app.exception, [str(exc.message) for exc in app.exception]
    assert len(app.metric) >= 4
    # In the hosted public mode only fictional checked-in documents can be used.
    if public_demo:
        assert len(app.file_uploader) == 0
        assert any("Public demo" in item.value for item in app.success)
    else:
        assert len(app.file_uploader) == 3

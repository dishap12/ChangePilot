"""Public, read-only Streamlit entrypoint for the ChangePilot portfolio demo.

Point Streamlit Community Cloud at public_demo.py (not app.py).
The public mode is forced on before the main application runs, even if
the hosting environment contains a conflicting setting.
"""
from pathlib import Path
import os
import runpy

os.environ["CHANGEPILOT_PUBLIC_DEMO"] = "true"
runpy.run_path(str(Path(__file__).resolve().with_name("app.py")), run_name="__main__")

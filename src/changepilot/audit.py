"""Local-only SQLite review audit trail (not suitable for shared public deployment)."""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ACTIONS = {"Approve for implementation", "Request clarification", "Reject proposal"}


def initialize(db_path: str | Path) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id TEXT NOT NULL,
            requirement_id TEXT NOT NULL,
            action TEXT NOT NULL,
            reviewer TEXT NOT NULL,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")


def add_decision(db_path: str | Path, requirement_id: str, action: str,
                 reviewer: str, note: str, workspace_id: str = "demo") -> None:
    if not workspace_id.strip():
        raise ValueError("Workspace ID is required.")
    if action not in ACTIONS:
        raise ValueError("Unsupported review decision.")
    if not reviewer.strip():
        raise ValueError("Reviewer name is required.")
    if not requirement_id.startswith("REQ-"):
        raise ValueError("Invalid requirement ID.")
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""INSERT INTO decisions (workspace_id, requirement_id, action, reviewer, note, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                     (workspace_id, requirement_id, action, reviewer.strip(), note.strip(),
                      datetime.now(timezone.utc).isoformat(timespec="seconds")))


def list_decisions(db_path: str | Path, workspace_id: str = "demo") -> list[dict]:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM decisions WHERE workspace_id = ? ORDER BY id DESC", (workspace_id,)).fetchall()
        return [dict(row) for row in rows]

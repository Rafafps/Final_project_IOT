"""
Lightweight storage layer for AQUA_SENSE.

Responsibilities:
- Create and manage a small SQLite database for telemetry and alerts.
- Provide helper methods to store and fetch data for the REST API and rules engine.

The goal is to keep persistence simple but reliable enough for the demo.
"""
from __future__ import annotations
import json
import sqlite3
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_FILE = Path(__file__).resolve().parent / "aqua_sense.db"

class Storage:
    """Thread-safe, minimal SQLite wrapper."""

    def __init__(self, db_path: Path = DB_FILE):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT NOT NULL,
                    device_type TEXT NOT NULL,
                    ts TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT,
                    alert_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    ts TEXT NOT NULL,
                    payload TEXT
                );
                """
            )
            conn.commit()

    def save_telemetry(self, device_id: str, device_type: str, ts: str, payload: Dict[str, Any]) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO telemetry (device_id, device_type, ts, payload) VALUES (?, ?, ?, ?)",
                (device_id, device_type, ts, json.dumps(payload)),
            )
            conn.commit()

    def get_telemetry(self, device_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        query = "SELECT * FROM telemetry"
        params: List[Any] = []
        if device_id:
            query += " WHERE device_id = ?"
            params.append(device_id)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def save_alert(
        self,
        alert_type: str,
        message: str,
        ts: str,
        device_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO alerts (device_id, alert_type, message, ts, payload) VALUES (?, ?, ?, ?, ?)",
                (device_id, alert_type, message, ts, json.dumps(payload or {})),
            )
            conn.commit()

    def get_alerts(self, limit: int = 100) -> List[Dict[str, Any]]:
        query = "SELECT * FROM alerts ORDER BY id DESC LIMIT ?"
        with self._connect() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
        return [self._row_to_dict(row) for row in rows]

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        data = dict(row)
        if "payload" in data and data["payload"]:
            try:
                data["payload"] = json.loads(data["payload"])
            except json.JSONDecodeError:
                pass
        return data


storage = Storage()
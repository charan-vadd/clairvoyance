"""Small timing helper for Daily voice startup instrumentation."""

from __future__ import annotations

import time
from typing import Any, Optional

from app.core.logger import logger

STARTED_AT_EPOCH_MS_KEY = "daily_startup_started_at_epoch_ms"


class DailyStartupTimer:
    """Emit grep-friendly timing marks for one Daily startup path."""

    def __init__(
        self,
        *,
        component: str,
        lead_id: Optional[str] = None,
        session_id: Optional[str] = None,
        started_at_epoch_ms: Optional[float] = None,
    ) -> None:
        self.component = component
        self.lead_id = lead_id
        self.session_id = session_id
        self.started_at_epoch_ms = started_at_epoch_ms
        self._start = time.perf_counter()
        self._last = self._start

    @classmethod
    def from_runner_body(
        cls,
        body: dict[str, Any],
        *,
        component: str,
    ) -> "DailyStartupTimer":
        started_at = body.get(STARTED_AT_EPOCH_MS_KEY)
        return cls(
            component=component,
            lead_id=str(body.get("lead_id")) if body.get("lead_id") else None,
            session_id=(
                str(body.get("session_id")) if body.get("session_id") else None
            ),
            started_at_epoch_ms=(
                float(started_at) if isinstance(started_at, (int, float)) else None
            ),
        )

    def mark(self, phase: str, **fields: Any) -> None:
        now = time.perf_counter()
        elapsed_ms = (now - self._start) * 1000
        delta_ms = (now - self._last) * 1000
        self._last = now

        parts = [
            "[daily-startup]",
            f"component={self.component}",
            f"phase={phase}",
            f"elapsed_ms={elapsed_ms:.1f}",
            f"delta_ms={delta_ms:.1f}",
        ]
        if self.started_at_epoch_ms is not None:
            total_ms = time.time() * 1000 - self.started_at_epoch_ms
            parts.append(f"total_since_connect_ms={total_ms:.1f}")
        if self.lead_id:
            parts.append(f"lead_id={self.lead_id}")
        if self.session_id:
            parts.append(f"session_id={self.session_id}")
        for key, value in fields.items():
            if value is not None:
                parts.append(f"{key}={value}")

        logger.info(" ".join(parts))

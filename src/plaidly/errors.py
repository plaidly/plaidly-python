"""Typed exceptions raised by the Plaidly SDK."""

from __future__ import annotations

from typing import Optional

import httpx


class PlaidlyError(Exception):
    """Raised when the Plaidly API returns a non-2xx response.

    Attributes:
        status: HTTP status code of the response.
        code: Application error code from the API ``Error.code`` field, if any.
        message: Human-readable error message from the API ``Error.message``.
    """

    def __init__(
        self,
        message: str,
        status: int,
        code: Optional[int] = None,
        response: Optional[httpx.Response] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.response = response

    def __str__(self) -> str:
        prefix = f"[{self.status}]"
        if self.code is not None:
            prefix += f" (code {self.code})"
        return f"{prefix} {self.message}"

    @classmethod
    def from_response(cls, response: httpx.Response) -> "PlaidlyError":
        """Build a :class:`PlaidlyError` from a failed HTTP response.

        Parses the API ``Error`` body (``{code, message}``) when present and
        falls back to the raw response text otherwise.
        """
        code: Optional[int] = None
        message = response.text or response.reason_phrase or "request failed"
        try:
            body = response.json()
        except (ValueError, TypeError):
            body = None
        if isinstance(body, dict):
            raw_code = body.get("code")
            if isinstance(raw_code, int):
                code = raw_code
            if body.get("message"):
                message = str(body["message"])
        return cls(
            message=message,
            status=response.status_code,
            code=code,
            response=response,
        )

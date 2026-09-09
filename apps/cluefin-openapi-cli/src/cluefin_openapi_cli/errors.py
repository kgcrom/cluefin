"""Structured error taxonomy for agent consumers.

Exit codes are the contract an agent branches on; the JSON envelope carries the
detail. Keep the table below in sync with README.md and SKILL.md.
"""

from __future__ import annotations

from typing import Any

EXIT_OK = 0
EXIT_UNEXPECTED = 1
EXIT_USAGE = 2
EXIT_CREDENTIALS = 3
EXIT_BROKER = 4
EXIT_RATE_LIMIT = 5

EXIT_CODES: dict[int, str] = {
    EXIT_OK: "success",
    EXIT_UNEXPECTED: "unexpected failure inside the CLI or client; not safe to retry blindly",
    EXIT_USAGE: "usage or validation error; fix the arguments, do not retry as-is",
    EXIT_CREDENTIALS: "credentials missing or rejected; check .env / environment, do not retry",
    EXIT_BROKER: "broker API, network, or timeout error; retry only if `retryable` is true",
    EXIT_RATE_LIMIT: "rate limited by the broker; wait `retry_after` seconds (or >= 1s) and retry",
}


class CliError(Exception):
    def __init__(
        self,
        message: str,
        *,
        exit_code: int = EXIT_UNEXPECTED,
        data: dict[str, Any] | None = None,
        error_type: str | None = None,
        retryable: bool = False,
        hint: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
        self.data = data or {}
        self.error_type = error_type or type(self).__name__
        self.retryable = retryable
        self.hint = hint

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "type": self.error_type,
            "message": self.message,
            "exit_code": self.exit_code,
            "retryable": self.retryable,
        }
        if self.hint:
            payload["hint"] = self.hint
        payload["data"] = self.data
        return {"error": payload}


def _class_names(exc: BaseException) -> list[str]:
    return [klass.__name__ for klass in type(exc).__mro__]


def classify_exception(exc: BaseException, *, command: str, broker: str) -> CliError:
    """Map a broker-client exception onto the CLI exit-code taxonomy.

    Matching is by class-name suffix so kis/kiwoom/dart exception hierarchies (which
    are parallel copies, not shared) all land in the same buckets.
    """

    names = _class_names(exc)
    message = str(exc) or type(exc).__name__
    data: dict[str, Any] = {"command": command, "broker": broker, "exception": type(exc).__name__}

    status = getattr(exc, "status_code", None)
    if status is not None:
        data["status_code"] = status
    response_data = getattr(exc, "response_data", None)
    if isinstance(response_data, dict):
        for key in ("rt_cd", "msg_cd", "msg1", "return_code", "return_msg", "status", "message"):
            if key in response_data:
                data[key] = response_data[key]
    return_code = getattr(exc, "return_code", None)
    if return_code is not None:
        data["return_code"] = return_code

    if any(name.endswith("RateLimitError") for name in names):
        retry_after = getattr(exc, "retry_after", None)
        if retry_after is not None:
            data["retry_after"] = retry_after
        return CliError(
            message,
            exit_code=EXIT_RATE_LIMIT,
            data=data,
            error_type="RateLimitError",
            retryable=True,
            hint="Wait retry_after seconds (default 1s) before calling any command for this broker again.",
        )

    if any(name.endswith(("AuthenticationError", "AuthorizationError")) for name in names):
        return CliError(
            message,
            exit_code=EXIT_CREDENTIALS,
            data=data,
            error_type="AuthenticationError",
            hint="Token was rejected. Check the *_APP_KEY / *_SECRET_KEY pair and *_ENV (dev vs prod) for this broker.",
        )

    if isinstance(exc, ValueError) and "credentials not configured" in message:
        return CliError(
            message,
            exit_code=EXIT_CREDENTIALS,
            data=data,
            error_type="CredentialsMissing",
            hint="Set the broker's credentials in .env (current working directory) or the environment. "
            "Run `brokers --json` to see which brokers are configured.",
        )

    if any(name.endswith(("TimeoutError", "NetworkError", "ServerError")) for name in names):
        return CliError(
            message,
            exit_code=EXIT_BROKER,
            data=data,
            error_type="BrokerUnavailable",
            retryable=True,
            hint="Transient broker/network failure. Retry once after a short pause.",
        )

    if type(exc).__name__ == "ValidationError" and callable(getattr(exc, "errors", None)):
        # pydantic: the broker answered, but the body did not fit the client's response model.
        # Almost always an unknown code / empty result, not a parameter problem.
        try:
            error_items = list(exc.errors())  # type: ignore[attr-defined]
        except Exception:  # pragma: no cover - defensive
            error_items = []
        data["fields"] = [".".join(str(part) for part in item.get("loc", ())) for item in error_items][:20]
        data["error_count"] = len(error_items)
        model = getattr(exc, "title", None)
        if model:
            data["model"] = model
        return CliError(
            f"Broker response did not match the client model ({len(error_items)} field errors).",
            exit_code=EXIT_BROKER,
            data=data,
            error_type="ResponseParseError",
            hint="The broker returned a sparse or empty body. Check that the code exists (e.g. `kis stock "
            "basic-info`) and that the market is open for this data; if the code is valid, the response "
            "model in cluefin-openapi may need updating.",
        )

    if any(name.endswith("ValidationError") for name in names):
        return CliError(
            message,
            exit_code=EXIT_BROKER,
            data=data,
            error_type="BrokerRejectedRequest",
            hint="The broker rejected the parameters. Re-read `schema <command>` and check enum/code values.",
        )

    if any(name.endswith("APIError") for name in names) or (isinstance(exc, ValueError) and "API Error" in message):
        return CliError(
            message,
            exit_code=EXIT_BROKER,
            data=data,
            error_type="BrokerApiError",
            hint="The broker returned an error body. Check msg1/return_msg; a market-hours or "
            "unsupported-on-mock restriction is common.",
        )

    return CliError(
        f"Command `{command}` failed: {message}",
        exit_code=EXIT_UNEXPECTED,
        data=data,
        error_type="ExecutionError",
    )

"""Shared HTTP-client infrastructure for kis, dart, and kiwoom clients."""

import json
import time
from typing import Callable, Dict, Optional

import requests


class BaseHttpClient:
    """Mixin holding request helpers shared by all broker HTTP clients."""

    def _safe_json(self, response: requests.Response) -> Optional[Dict]:
        """Safely parse a JSON response, returning None if parsing fails."""
        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
            return None

    def _get_retry_after(self, response: requests.Response) -> Optional[int]:
        """Extract the Retry-After header as an int, or None."""
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return int(retry_after)
            except ValueError:
                pass
        return None

    def _execute_with_retry(
        self,
        send_fn: Callable[[], requests.Response],
        *,
        rate_limiter,
        timeout: int,
        max_retries: int,
        request_context: dict,
        dispatch: Callable[[requests.Response], Optional[Exception]],
        rate_limit_error: Callable[[], Exception],
        timeout_error: Callable[[Exception], Exception],
        network_error: Callable[[Exception], Exception],
        on_response: Optional[Callable[[requests.Response, dict], None]] = None,
        retry_after_provider: Optional[Callable[[requests.Response], Optional[int]]] = None,
    ) -> requests.Response:
        """Shared rate-limit pre-flight, attempt loop, status dispatch, and backoff.

        Parameters
        ----------
        send_fn:
            Callable that performs the actual HTTP call and returns a Response.
        rate_limiter:
            TokenBucket; must pass wait_for_tokens(timeout=timeout) before sending.
        timeout:
            Seconds used for the token-bucket wait timeout.
        max_retries:
            Number of retries beyond the first attempt (total attempts = max_retries+1).
        request_context:
            Already-redacted dict describing the request (for side-effect hooks).
        dispatch:
            Called with the response for every non-200 status. Returns an Exception
            to raise (immediately for 4xx/unexpected, or on final retry for 429/5xx),
            or None to accept the response and return it.
        rate_limit_error:
            Factory () -> Exception raised when the token bucket times out.
        timeout_error:
            Factory (e) -> Exception raised on requests.Timeout exhaustion.
        network_error:
            Factory (e) -> Exception raised on ConnectionError exhaustion or
            RequestException.
        on_response:
            Optional hook called on every received response before status branching.
        retry_after_provider:
            Optional callable to extract Retry-After from a 429 response;
            defaults to self._get_retry_after.
        """
        if not rate_limiter.wait_for_tokens(timeout=timeout):
            raise rate_limit_error()

        _retry_after_fn = retry_after_provider if retry_after_provider is not None else self._get_retry_after

        for attempt in range(max_retries + 1):
            try:
                response = send_fn()

                if on_response is not None:
                    on_response(response, request_context)

                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    retry_after = _retry_after_fn(response)
                    if attempt < max_retries:
                        wait_time = retry_after or (2**attempt)
                        time.sleep(wait_time)
                        continue
                    else:
                        raise dispatch(response)
                elif 500 <= response.status_code < 600:
                    if attempt < max_retries:
                        wait_time = 2**attempt
                        time.sleep(wait_time)
                        continue
                    else:
                        raise dispatch(response)
                else:
                    exc = dispatch(response)
                    if exc is not None:
                        raise exc
                    return response

            except requests.exceptions.Timeout as e:
                if attempt < max_retries:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue
                else:
                    raise timeout_error(e) from e
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue
                else:
                    raise network_error(e) from e
            except requests.exceptions.RequestException as e:
                raise network_error(e) from e

        # Should not be reached, but kept as a safety net
        raise network_error(RuntimeError("Maximum retries exceeded"))

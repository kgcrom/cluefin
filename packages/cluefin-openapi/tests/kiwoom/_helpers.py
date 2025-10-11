import inspect
from dataclasses import dataclass, field
from typing import Any, Dict
from unittest.mock import Mock


@dataclass
class EndpointCase:
    name: str
    method_name: str
    response_model_attr: str
    api_id: str
    call_kwargs: Dict[str, Any]
    expected_body: Dict[str, Any]
    response_payload: Dict[str, Any] = field(default_factory=lambda: {"return_code": 0, "return_msg": "OK"})
    cont_flag_key: str | None = "cont-yn"
    cont_flag_value: str = "N"
    next_key: str | None = ""


def build_mock_response(payload: Dict[str, Any], api_id: str, cont_yn: str, next_key: str) -> Mock:
    response = Mock()
    response.status_code = 200
    response.json.return_value = payload
    response.headers = {"cont-yn": cont_yn, "next-key": next_key, "api-id": api_id}
    response.text = "OK"
    return response


def make_dummy_model(captured_instances: list[Any]):
    class DummyResponseModel:
        def __init__(self, **kwargs: Any):
            self.kwargs = kwargs
            captured_instances.append(self)

        @classmethod
        def model_validate(cls, data: Dict[str, Any]):
            return cls(**data)

    return DummyResponseModel


def run_post_case(
    monkeypatch,
    module,
    api_cls,
    case: EndpointCase,
    base_headers: Dict[str, str],
):
    client = Mock()
    client.token = "test_token"
    response_next_key = case.next_key if case.next_key is not None else ""
    client._post.return_value = build_mock_response(
        case.response_payload,
        case.api_id,
        case.cont_flag_value,
        response_next_key,
    )

    captured_instances: list[Any] = []
    dummy_model = make_dummy_model(captured_instances)
    monkeypatch.setattr(module, case.response_model_attr, dummy_model)

    api = api_cls(client)
    method = getattr(api, case.method_name)
    call_kwargs = dict(case.call_kwargs)
    params = inspect.signature(method).parameters
    if case.cont_flag_key in {"cont-yn", "con-yn"} and "cont_yn" in params:
        call_kwargs.setdefault("cont_yn", case.cont_flag_value)
    elif case.cont_flag_key == "cont-yn" and "cont_yn" in params:
        call_kwargs.setdefault("cont_yn", case.cont_flag_value)
    if case.next_key is not None and "next_key" in params:
        call_kwargs.setdefault("next_key", case.next_key)
    result = method(**call_kwargs)

    client._post.assert_called_once()
    path, headers, body = client._post.call_args.args

    assert path == api.path
    expected_headers = {
        **base_headers,
        "Authorization": "Bearer test_token",
        "api-id": case.api_id,
    }
    if case.cont_flag_key:
        expected_headers[case.cont_flag_key] = case.cont_flag_value
    if case.next_key is not None:
        expected_headers["next-key"] = case.next_key
    assert headers == expected_headers
    assert body == case.expected_body

    assert len(captured_instances) == 1
    assert result.body is captured_instances[0]
    assert captured_instances[0].kwargs == case.response_payload
    assert result.headers.api_id == case.api_id
    assert result.headers.cont_yn == case.cont_flag_value
    assert result.headers.next_key == (response_next_key)

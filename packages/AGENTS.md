# AGENTS.md — packages

Libraries the apps build on; each has its own AGENTS.md. `cluefin-openapi-ts` is the TypeScript sibling of
`cluefin-openapi` and shares its token cache files. `cluefin-sec-notes` is not published to PyPI.

## Type checking

- `uv run pyright` (basic) covers only the `[tool.pyright] include` list in the root `pyproject.toml`; packages are
  added once their errors are 0, so a package not in the list is unchecked, not clean.
- Annotate return types of shared helpers. #196 changed `dart/_client.py`'s `_request` so its inferred type became
  `dict | Any | bytes`; pyright on that file was clean and main failed in two untouched DART modules (2026-11-02).
- pydantic models with `populate_by_name` still type-check against the alias only, so construct them by alias.

## Notebooks

`examples/*.ipynb` 는 커밋 전에 output·execution_count 를 지운다(출력에 계좌번호가 섞일 수 있다). 저장소 루트에서:
`uv run --with jupyter jupyter nbconvert --clear-output --inplace packages/<패키지>/examples/<노트북>.ipynb`

## Codacy findings in Python (apps included)

- **Any `import` from the stdlib `xml` package is critical** (XXE), even type-only under `TYPE_CHECKING` or
  `xml.parsers.expat.errors`. Use a `Protocol` with the element methods you need (`cluefin_dart_notes/_xml.py`) and
  literal expat constants. Parse with `defusedxml` and keep it (decided 2026-10): the bundled expat on 3.10–3.14 is
  2.6.3, which Python's docs call possibly vulnerable to entity-expansion DoS; defusedxml forbids entity
  declarations. Its last stable release, 0.7.1, works on 3.10–3.14.
- **Nested quantifiers in a regex are critical** ("inefficient regular expression"), e.g.
  `{N}(?:\.?(?:\s*(?:,|and|&))+\s*{N})*`. Keep each regex flat and loop with `pattern.match(text, pos)`
  (`_read_numbers` in `cluefin_sec_notes/_labels.py`).
- `importlib.import_module(<non-literal>)` is critical, tests included (#186). Scan the source with `ast` instead,
  as `cluefin-openapi/tests/test_response_models_unit.py` does.
- A mutable default argument is high, tests included. Use a tuple.
- A stdlib logger call whose message mentions token/secret/key **and** passes `%s` args is high ("hardcoded secret
  being logged"), even when the arg is a timestamp (6 in the Kiwoom token manager, #181). Use an f-string and never
  log the token itself.

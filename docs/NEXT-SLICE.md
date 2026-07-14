# Next slice — deferred from review

Findings from the whole-branch review that are real but out of scope for the current
fix pass (no behavior change intended there). Tracked here so they don't evaporate.

- `gen_vault.py`'s `overwrite=False` edit-preserving path is not reachable from the
  CLI (`__main__` always calls `gen_vault(..., overwrite=True)` implicitly via the
  default). Wire a `--no-overwrite` flag through `__main__`, or drop the `overwrite`
  param entirely if the preserve-on-rerun behavior isn't actually needed.
- `init_channel.py` interpolates `cfg` and `plugin_dir` into the `bin/yt` bash wrapper
  via plain f-string formatting, without shell-escaping. Low risk today (both come from
  a constrained ID charset / the plugin's own path), but if either input source changes,
  use `shlex.quote()` when this file is next touched.
- `verify_links` (in `scripts/verify_links.py`) doesn't detect staleness of preserved
  files (kept via `overwrite=False`) versus changed templates — a preserved file can
  silently drift from its template.
- Unterminated ``` fences in generated docs aren't stripped/validated.
- `gen_vault.py`'s `_render()` doesn't sanitize `{{` sequences that come from user
  input in the briefing — a user-provided value containing `{{other_key}}` could get
  substituted unexpectedly on a subsequent pass.
- `init_channel.py`'s `chmod` on `bin/yt` sets `S_IXUSR | S_IXGRP` but omits
  `S_IXOTH` — inconsistent with the intent of a user-executable wrapper script.
- `tests/test_config_dir.py` stubs modules via global `sys.modules` mutation instead
  of proper fixtures/mocks — works but is fragile if tests run in a different order or
  in parallel.

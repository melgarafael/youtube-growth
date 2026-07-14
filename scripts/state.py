#!/usr/bin/env python3
"""Estado de progresso do onboarding (idempotencia/resume)."""
import os, json, tempfile

def _path(user_dir):
    d = os.path.join(user_dir, ".youtube-growth")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "state.json")

def state_get(user_dir):
    p = _path(user_dir)
    if not os.path.exists(p):
        return {}
    with open(p) as f:
        return json.load(f)

def state_set(user_dir, **kw):
    s = state_get(user_dir)
    s.update(kw)
    p = _path(user_dir)
    # Write to temp file in same directory, then atomically replace
    with tempfile.NamedTemporaryFile(mode='w', dir=os.path.dirname(p), delete=False, suffix='.tmp') as tmp:
        json.dump(s, tmp, indent=2)
        tmp_path = tmp.name
    os.replace(tmp_path, p)
    return s

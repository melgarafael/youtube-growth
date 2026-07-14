#!/usr/bin/env python3
"""Estado de progresso do onboarding (idempotencia/resume)."""
import os, json

def _path(user_dir):
    d = os.path.join(user_dir, ".youtube-growth")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "state.json")

def state_get(user_dir):
    p = _path(user_dir)
    return json.load(open(p)) if os.path.exists(p) else {}

def state_set(user_dir, **kw):
    s = state_get(user_dir)
    s.update(kw)
    json.dump(s, open(_path(user_dir), "w"), indent=2)
    return s

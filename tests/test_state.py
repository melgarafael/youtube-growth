import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from state import state_get, state_set

def test_roundtrip(tmp_path):
    assert state_get(str(tmp_path)) == {}
    state_set(str(tmp_path), briefing_done=True)
    assert state_get(str(tmp_path))["briefing_done"] is True

def test_merges_not_clobbers(tmp_path):
    state_set(str(tmp_path), briefing_done=True)
    state_set(str(tmp_path), connected=True)
    s = state_get(str(tmp_path))
    assert s["briefing_done"] is True and s["connected"] is True

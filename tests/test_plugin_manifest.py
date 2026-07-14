import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_manifest_valid():
    p = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
    assert p["name"] == "youtube-growth"
    assert "version" in p and "description" in p

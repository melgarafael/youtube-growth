import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from verify_links import verify_links

def test_detects_broken_link(tmp_path):
    (tmp_path / "a.md").write_text("liga pra [[inexistente]]", encoding="utf-8")
    r = verify_links(str(tmp_path))
    assert ("a.md", "inexistente") in r["broken"]

def test_clean_vault(tmp_path):
    (tmp_path / "a.md").write_text("liga pra [[b]]", encoding="utf-8")
    (tmp_path / "b.md").write_text("volta pra [[a]]", encoding="utf-8")
    r = verify_links(str(tmp_path))
    assert r["broken"] == [] and r["orphans"] == []

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

def test_ambiguous_basename_credits_all_candidates(tmp_path):
    (tmp_path / "dir_a").mkdir()
    (tmp_path / "dir_b").mkdir()
    (tmp_path / "dir_a" / "note.md").write_text("sem links", encoding="utf-8")
    (tmp_path / "dir_b" / "note.md").write_text("sem links", encoding="utf-8")
    (tmp_path / "c.md").write_text("ambiguo [[note]]", encoding="utf-8")
    r = verify_links(str(tmp_path))
    assert os.path.join("dir_a", "note.md") not in r["unreachable"]
    assert os.path.join("dir_b", "note.md") not in r["unreachable"]

def test_unreachable_detects_note_with_outgoing_but_no_incoming(tmp_path):
    (tmp_path / "a.md").write_text("[[b]]", encoding="utf-8")
    (tmp_path / "b.md").write_text("[[a]]", encoding="utf-8")
    (tmp_path / "lonely.md").write_text("[[a]]", encoding="utf-8")
    r = verify_links(str(tmp_path))
    assert "lonely.md" in r["unreachable"]
    assert "a.md" not in r["unreachable"]
    assert "b.md" not in r["unreachable"]

def test_fenced_code_block_links_ignored(tmp_path):
    (tmp_path / "a.md").write_text(
        "texto\n```\n[[foo]]\n```\nfim", encoding="utf-8"
    )
    r = verify_links(str(tmp_path))
    assert ("a.md", "foo") not in r["broken"]

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from gen_vault import gen_vault

BRIEF = {"canal_nome": "Cozinha da Ana", "canal_handle": "@cozinhadaana",
         "nicho": "receitas rápidas", "objetivo": "alcance",
         "diferencial": "sem glúten de verdade", "monetiza": ""}

def test_generates_core_files(tmp_path):
    gen_vault(BRIEF, str(tmp_path))
    for f in ["_INDEX.md", "perfil-canal.md", "metas.md",
              "benchmark/_MOC.md", "drafts/_MOC.md", "thumbnail-lab/_MOC.md"]:
        assert (tmp_path / f).exists(), f

def test_no_unfilled_placeholders(tmp_path):
    gen_vault(BRIEF, str(tmp_path))
    for dp, _, fns in os.walk(tmp_path):
        for fn in fns:
            txt = open(os.path.join(dp, fn), encoding="utf-8").read()
            assert "{{" not in txt, f"placeholder solto em {fn}"

def test_passes_link_verifier(tmp_path):
    from verify_links import verify_links
    gen_vault(BRIEF, str(tmp_path))
    r = verify_links(str(tmp_path))
    assert r["broken"] == [] and r["orphans"] == [] and r["unreachable"] == []

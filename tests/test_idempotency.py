import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from gen_vault import gen_vault

BRIEF = {"canal_nome": "X", "canal_handle": "@x", "nicho": "n",
         "objetivo": "alcance", "diferencial": "d", "monetiza": ""}

def test_regen_preserves_user_edits(tmp_path):
    gen_vault(BRIEF, str(tmp_path))
    perfil = tmp_path / "perfil-canal.md"
    perfil.write_text(perfil.read_text() + "\n\nMINHA EDIÇÃO", encoding="utf-8")
    # segundo run NÃO deve sobrescrever conteúdo editado pelo usuário
    gen_vault(BRIEF, str(tmp_path), overwrite=False)
    assert "MINHA EDIÇÃO" in perfil.read_text()

import os, sys, importlib
from unittest.mock import MagicMock
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

# Mock Google libraries before importing yt_auth
sys.modules["google_auth_oauthlib"] = MagicMock()
sys.modules["google_auth_oauthlib.flow"] = MagicMock()
sys.modules["google.auth"] = MagicMock()
sys.modules["google.auth.transport"] = MagicMock()
sys.modules["google.auth.transport.requests"] = MagicMock()
sys.modules["google.oauth2"] = MagicMock()
sys.modules["google.oauth2.credentials"] = MagicMock()
sys.modules["googleapiclient"] = MagicMock()
sys.modules["googleapiclient.discovery"] = MagicMock()
sys.modules["googleapiclient.http"] = MagicMock()

def test_base_uses_env(tmp_path, monkeypatch):
    monkeypatch.setenv("YTG_CONFIG_DIR", str(tmp_path))
    sys.modules.pop("yt_auth", None)
    ya = importlib.import_module("yt_auth")
    importlib.reload(ya)
    assert ya.BASE == str(tmp_path)
    assert ya.TOKEN == os.path.join(str(tmp_path), "token.json")

def test_base_default_without_env(monkeypatch):
    monkeypatch.delenv("YTG_CONFIG_DIR", raising=False)
    sys.modules.pop("yt_auth", None)
    ya = importlib.import_module("yt_auth")
    importlib.reload(ya)
    assert ya.BASE == os.path.expanduser("~/.youtube-seo")

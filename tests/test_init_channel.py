import os, sys, stat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from init_channel import init_channel

def test_creates_config_and_wrapper(tmp_path, monkeypatch):
    home = tmp_path / "home"; home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    user_dir = tmp_path / "meu-canal"; user_dir.mkdir()
    cfg = init_channel("UC123", str(user_dir), plugin_dir="/plugins/youtube-growth")
    assert os.path.isdir(cfg)
    wrapper = user_dir / "bin" / "yt"
    assert wrapper.exists()
    content = wrapper.read_text()
    assert "UC123" in content and "/plugins/youtube-growth/scripts/yt.py" in content
    assert os.stat(wrapper).st_mode & stat.S_IXUSR  # executável

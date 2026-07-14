#!/usr/bin/env python3
"""Prepara o config dir do canal e escreve o wrapper bin/yt no dir do usuario."""
import os, sys, stat

def init_channel(channel_id, user_dir, plugin_dir=None):
    plugin_dir = plugin_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cfg = os.path.join(os.path.expanduser("~/.config/youtube-growth"), channel_id)
    os.makedirs(cfg, exist_ok=True)
    os.chmod(cfg, 0o700)
    bindir = os.path.join(user_dir, "bin")
    os.makedirs(bindir, exist_ok=True)
    wrapper = os.path.join(bindir, "yt")
    with open(wrapper, "w") as f:
        f.write("#!/usr/bin/env bash\n"
                f'export YTG_CONFIG_DIR="{cfg}"\n'
                f'exec "$YTG_CONFIG_DIR/.venv/bin/python" "{plugin_dir}/scripts/yt.py" "$@"\n')
    os.chmod(wrapper, os.stat(wrapper).st_mode | stat.S_IXUSR | stat.S_IXGRP)
    return cfg

if __name__ == "__main__":
    print(init_channel(sys.argv[1], sys.argv[2]))

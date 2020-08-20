### Installation
```bash
./install.sh
# symlinks:
# - ./blinkmon.sh to /usr/local/bin/blinkmon
# - ./systemd/* to ~/.config/systemd/user/*

systemctl --user enable blinkmon.service
systemctl --user start blinkmon
```

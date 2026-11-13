#!/bin/bash
# Cloud Workstations runs /etc/workstation-startup.d/* as root at every start.
# Tells the Toolbox Agent that PyCharm is already installed at /opt/jetbrains,
# so the Toolbox App on the laptop opens it instead of downloading a backend.
# Written at every start because /home is a cache, not part of the image.
set -euo pipefail

user_home=/home/user
dir="$user_home/.local/share/JetBrains/Toolbox/preinstalled"
mkdir -p "$dir"
echo '{"installationDirectory": "/opt/jetbrains/pycharm"}' > "$dir/pycharm.json"
chown -R user:user "$user_home/.local"

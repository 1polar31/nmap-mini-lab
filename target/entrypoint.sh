#!/bin/bash

echo "[*] Starting target services..."

# Port 21 — fake FTP server. The flag is hidden in this banner.
# Nmap -sV will grab the banner and parse it as the version string.
python3 /banner_server.py 21 ftp \
    "220 ProFTPD 1.3.5-FLAG{nmap_service_version_detection} Server (NovaCorp FTP)" &

# Port 22 — fake SSH banner (no flag, just realism)
python3 /banner_server.py 22 ssh \
    "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5" &

# Port 80 — fake HTTP server (no flag, just realism)
python3 /banner_server.py 80 http \
    "Apache/2.4.41 (Ubuntu)" &

# Port 8080 — fake HTTP-proxy (no flag, just realism)
python3 /banner_server.py 8080 http \
    "nginx/1.18.0" &

echo "[*] Target ready on ports 21, 22, 80, 8080"

# Keep container alive
wait

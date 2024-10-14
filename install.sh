#!/bin/bash

# 檢查是否以 root 權限運行
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# 安裝必要的依賴項（如果需要，這裡以 Python 為例）
apt-get update
apt-get install -y python3

# 複製 Python 腳本到 /usr/local/bin
INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="magic_packet.py"
cp $SCRIPT_NAME $INSTALL_DIR

# 確保腳本可執行
chmod +x $INSTALL_DIR/$SCRIPT_NAME

# 設定 systemd 服務
SERVICE_FILE="/etc/systemd/system/forward_magic_packet.service"

# 如果服務文件已存在，提示用戶
if [ -f "$SERVICE_FILE" ]; then
  echo "$SERVICE_FILE already exists. Do you want to overwrite it? (y/n)"
  read answer
  if [ "$answer" != "${answer#[Yy]}" ] ;then
    echo "Overwriting $SERVICE_FILE..."
  else
    echo "Installation cancelled."
    exit 1
  fi
fi

# 寫入 systemd 服務文件
cat <<EOL > $SERVICE_FILE
[Unit]
Description=Forward Magic Packet Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $INSTALL_DIR/$SCRIPT_NAME
Restart=always
User=root
WorkingDirectory=$INSTALL_DIR
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOL

# 重新加載 systemd 並啟動服務
systemctl daemon-reload
systemctl enable forward_magic_packet.service
systemctl start forward_magic_packet.service

echo "Installation completed. The forward_magic_packet service is now running."

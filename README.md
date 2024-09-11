本專案專門針對有需要在遠端將家中或公司內區域網路電腦進行遠端喚醒的作業。

建置步驟：
  1. 區域網路內部其中一部 Linux 系統需下載本程式碼並設為開機時啟動
  2. 該 Linux 需先安裝 python 3
  3. 需要前端防火牆轉送 UDP 埠號 9 到該 Linux

要在每次開機時自動執行你的 magic_packet.py 程式，你可以選擇以下幾種方法來實現：使用 systemd 建立服務、修改 rc.local 檔案或使用 cron 的 @reboot 功能。以下是這三種方法的詳細步驟：

方法 1: 使用 systemd 建立服務
systemd 是現代 Linux 系統中用來管理系統和服務的工具。使用 systemd 可以非常靈活地控制指令碼的啟動、停止和自動重新啟動。

1. 建立一個 systemd 服務檔案
開啟終端設備機，然後使用 nano 或其他純文字編輯器建立一個新的服務檔案。例如，使用 nano 編輯器：

sudo nano /etc/systemd/system/forward_magic_packet.service
在檔案中加入 orward_magic_packet.service 的內容（假設 Python 指令碼的位置是 /home/your_username/magic_packet.py）：

Description: 給服務一個描述名稱。
After: 確保網路服務啟動後才啟動此指令碼。
ExecStart: 指定執行此服務的指令（用完整的 Python 路徑）。
Restart: 設定為 always，以便在指令碼崩潰或發生錯誤後自動重新啟動。
User: 設定為 root，確保使用 root 權限執行。
儲存並離開編輯器：在 nano 中，按 Ctrl + X，然後按 Y 確認儲存並離開。

2. 啟用並啟動服務
重新載入 systemd 來讀取新的服務檔案：
sudo systemctl daemon-reload
啟用服務，使其在開機時自動啟動：
sudo systemctl enable forward_magic_packet.service
立即啟動服務：
sudo systemctl start forward_magic_packet.service
檢查服務狀態：
sudo systemctl status forward_magic_packet.service
如果服務執行正常，你會看到服務狀態顯示為 active (running)。

方法 2: 修改 rc.local 檔案
這種方法適合於需要在開機時簡單執行指令的情況。注意，某些較新的 Linux 發行版本可能不再使用 rc.local。

開啟 rc.local 檔案進行編輯：
sudo nano /etc/rc.local
在 exit 0 之前加入以下行（假設你的指令碼路徑是 /home/your_username/magic_packet.py）：
/usr/bin/python3 /home/your_username/magic_packet.py &
& 使指令碼在背景執行。

儲存並離開編輯器。

給 rc.local 檔案執行權限（如果沒有）：

sudo chmod +x /etc/rc.local
重新啟動系統檢查指令碼是否執行。

方法 3: 使用 cron 的 @reboot 功能
cron 是 Linux 中用來安排定時工作的工具。@reboot 可以在每次系統啟動時執行指令。

編輯 crontab 檔案：

sudo crontab -e
在 crontab 檔案中加入以下行（假設指令碼路徑是 /home/your_username/magic_packet.py）：

@reboot /usr/bin/python3 /home/your_username/magic_packet.py
儲存並離開編輯器。

重新啟動系統檢查指令碼是否執行。

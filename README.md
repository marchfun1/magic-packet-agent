本專案專門針對有需要在遠端將家中或公司內區域網路電腦進行遠端喚醒的作業。利用在區域網路中的 Linux 安裝本程式以作為 magic packet (魔術封包) 的轉送站。  

建置步驟：
  1. 區域網路內部其中一部 Linux 系統需安裝本程式
  2. 需要 python 3 (本程式會自動安裝)  
  3. 需要前端防火牆轉送 UDP 埠號 9 到該 Linux

安裝指令：(依序執行以下指令)  
  
git clone https://github.com/marchfun1/magic-packet-forwarder.git  

cd magic-packet-forwarder  

chmod +x install.sh  

sudo ./install.sh  
  
即可安裝為系統服務。    

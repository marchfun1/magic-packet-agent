本專案專門針對有需要在遠端將家中或公司內區域網路電腦進行遠端喚醒的作業。利用在區域網路中的 Linux 安裝本程式以作為 magic packet (魔術封包) 的轉送站。  

建置步驟：
  1. 在區域網路內部其中一部 Linux 上安裝本程式
  2. 需要 python 3 (若未安裝則本程式會自動安裝)  
  3. 需要前端路由器轉送 UDP 埠號 9 到該 Linux
  4. 開放防火牆埠號 9  

若系統中尚未安裝 git 則需使用以下指令安裝：  
```
sudo apt install git
```

安裝指令：(依序執行以下指令)  
```
git clone https://github.com/marchfun1/magic-packet-agent.git
```
```
cd magic-packet-agent
```
```  
chmod +x install.sh
```
```
sudo ./install.sh
```

即可安裝為系統服務。    

----------------------------------------------------------------------------------------
(English)

This project is specifically designed for remote wake-on-LAN operations for computers in a home or company local area network. Install this program on a Linux machine within the LAN to serve as a relay station for the magic packet.  

Setup steps:  

  1. A Linux system within the LAN needs to install this program  
  2. Requires Python 3 (this program will automatically install it)
  3. Needs the front-end router to forward UDP port 9 to the Linux system
  4. Open firewall port 9  

If git is not installed in the system, you need to use the following command to install it:  
```
sudo apt install git
``` 

Installation commands (execute the following commands in order):
```
git clone https://github.com/marchfun1/magic-packet-agent.git
```
```
cd magic-packet-agent
```
```  
chmod +x install.sh
```
```
sudo ./install.sh
```

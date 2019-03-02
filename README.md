# ClassQuiz development blog

https://classquiz.wordpress.com/


# NodeMCU soft-brick repair

Press, and hold, the FLASH button on the NodeMCU.

Open a terminal and run:
sudo python ~/.local/bin/esptool.py --port /dev/ttyUSB0 write_flash 0x00000 /home/joao/Dropbox/UA/Tese/2019/Code/NodeMCU/v0/v0.ino

NOTE:
- esptool.py might be in a different directory;
- the port might be different;
- /home/joao/Dropbox/UA/Tese/2019/Code/NodeMCU/v0/v0.ino is the path to a blank sketch.
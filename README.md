# ClassQuiz development blog

https://classquiz.wordpress.com/


# NodeMCU soft-brick repair

Press, and hold, the FLASH button on the NodeMCU.

Open a terminal and run:

> sudo python ~/.local/bin/esptool.py --port /dev/ttyUSB0 write_flash 0x00000 /home/joao/Dropbox/UA/Tese/2019/quiz_dev/blank_firmware/blank_firmware.ino

Release the FLASH button after seeing "Connecting...".

NOTE:
- esptool.py might be in a different directory;
- the port might be different;
- /home/joao/Dropbox/UA/Tese/2019/quiz_dev/blank_firmware/blank_firmware.ino is the path to a blank sketch.
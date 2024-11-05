from PyQt6.QtCore import QThread
import subprocess

class Log(QThread):
    def run(self):
        subprocess.call("mkdir logs", creationflags=0x08000000, shell=True)
        subprocess.call("mkdir logs/minecraft-logs", creationflags=0x08000000, shell=True)
        subprocess.call("git clone https://github.com/vctorfarias/minecraft-log-1 ./logs/minecraft-logs", creationflags=0x08000000, shell=True)
        open("logs/git_pull_log.txt", "w")
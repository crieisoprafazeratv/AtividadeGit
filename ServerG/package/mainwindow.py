from PyQt6.QtWidgets import QMainWindow, QDialog
from PyQt6.QtGui import QMovie
from package.downloader import Downloader
from package.log import Log
from package.uploader import Uploader
from package.ui.mainwindow_ui import Ui_MainWindow
from package.ui import configdialog_ui, errordialog_ui, ownerdialog_ui
import subprocess
import datetime
import rust_modules


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        cato_gif = QMovie("assets/cato.gif")

        self.ui.cato.setMovie(cato_gif)
        cato_gif.start()

        self.ui.startServerBtn.clicked.connect(self.start_server)
        self.ui.downloadServerBtn.clicked.connect(self.download_server)
        self.ui.saveServerBtn.clicked.connect(self.upload_server)
        self.ui.configButton.clicked.connect(self.config_dialog)
        self.ui.changeOwnerBtn.clicked.connect(self.change_owner_dialog)

        rust_modules.pull_log_from_gith()

        self.show()

        if rust_modules.is_dir_empty(".\\logs"):
            self._log = Log()
            
            self._log.start()

        if rust_modules.is_dir_empty(".\\userconfig"):
            subprocess.call("mkdir userconfig", creationflags=0x08000000, shell=True)

            self.config_dialog()

    
    def start_server(self):
        user_file = open("./userconfig/user.properties", "r")
        user_file.readline()
        name = user_file.readline().replace('\n', '')

        if not rust_modules.is_owner(name):
            self.error_dialog("Tu não é o dono!")
            user_file.close()

            return

        user_file.readline()
        user_file.readline()
        ram = user_file.readline().replace('\n', '')

        rust_modules.start_server(ram)


    def download_server(self):
        if rust_modules.check_server_status() == "Offline":
            if not rust_modules.is_owner("jndf381kfd093"):
                self.error_dialog("Alguém ainda não deu upload no mapa\ndepois de baixar (provavelmente)!")

                return

            user_file = open("./userconfig/user.properties", "r")
            user_file.readline()
            name = user_file.readline().replace('\n', '')

            self.change_owner(name)

            user_file.close()

            self._downloader = Downloader()
            
            self._downloader.start()

            self.update_log("download")
            rust_modules.update_log()
        else:
            self.error_dialog("Server tá online, dê 'stop' antes de fazer download")

            return


    def upload_server(self):
        if rust_modules.check_server_status() == "Offline":
            user_file = open("./userconfig/user.properties", "r")
            user_file.readline()
            name = user_file.readline().replace('\n', '')

            if not rust_modules.is_owner(name):
                self.error_dialog("Tu não é o dono!")
                user_file.close()

                return
            
            self._uploader = Uploader()
            
            self._uploader.start()

            self.error = False
            self._uploader.error.connect(lambda: self.error_dialog("Diretório 'server' não se encontra nos arquivos"))

            user_file.close()

            if not self.error:
                self.change_owner("jndf381kfd093")

                self.update_log("upload")
                rust_modules.update_log()

                self.error = False
        else:
            self.error_dialog("Server tá online, dê 'stop' antes de fazer upload")

            return
    

    def get_time(self):
        date = datetime.datetime.now()

        return f"{date.day:02}/{date.month:02}/{date.year} {date.hour:02}:{date.minute:02}:{date.second:02}"


    # TODO
    def check_status(self):
        pass


    def error_dialog(self, error: str):
        dialog = QDialog()
        ui = errordialog_ui.Ui_Dialog()
        ui.setupUi(dialog)

        ui.error.setText(error)

        dialog.exec()

        self.error = True

    
    def config_dialog(self):
        dialog = QDialog()
        ui = configdialog_ui.Ui_Dialog()
        ui.setupUi(dialog)
        
        ui.counter.setText(str(ui.horizontalSlider.value()))

        ui.horizontalSlider.valueChanged.connect(lambda: self.update_slider_value(ui.horizontalSlider, ui.counter))

        ui.cancelBtn.clicked.connect(dialog.close)
        ui.saveBtn.clicked.connect(lambda: self.update_user_properties(ui.plainTextEdit.toPlainText(), ui.horizontalSlider.value()))
        ui.saveBtn.clicked.connect(dialog.close)

        dialog.exec()

    
    def update_slider_value(self, slider, counter):
        counter.setText(str(slider.value()))

    
    def update_user_properties(self, name, ram):
        f = open("./userconfig/user.properties", "w+")
        f.write(f"NOME: \n{name}\n\nRAM: \n{ram}G")

        f.close()

    
    def update_log(self, action: str):
        user_file = open("./userconfig/user.properties", "r")
        user_file.readline()
        user = user_file.readline().replace('\n', '')
        log_file = open("./logs/minecraft-logs/latest.txt", "a")
        log_file.write(f"\n{user} - {self.get_time()} - {action}")

        log_file.close()
        user_file.close()

    
    def change_owner_dialog(self):
        dialog = QDialog()
        ui = ownerdialog_ui.Ui_Dialog()
        ui.setupUi(dialog)

        ui.cancelBtn.clicked.connect(dialog.close)
        ui.okBtn.clicked.connect(lambda: self.change_owner(ui.textEdit.toPlainText()))
        ui.okBtn.clicked.connect(dialog.close)

        dialog.exec()

    
    def change_owner(self, new_owner: str):
        if new_owner == "":
            new_owner = "jndf381kfd093"

        with open("./logs/minecraft-logs/owner.txt", "w") as own_f:
            own_f.write(new_owner)
        
        rust_modules.update_log()

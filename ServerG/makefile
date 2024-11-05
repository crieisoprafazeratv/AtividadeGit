all:
	python -m PyQt6.uic.pyuic design\MainWindow_UI.ui -o package\ui\mainwindow_ui.py
	python -m PyQt6.uic.pyuic design\ConfigDialog_UI.ui -o package\ui\configdialog_ui.py
	python -m PyQt6.uic.pyuic design\ErrorDialog_UI.ui -o package\ui\errordialog_ui.py
	python -m PyQt6.uic.pyuic design\OwnerDialog_UI.ui -o package\ui\ownerdialog_ui.py
	maturin develop --release
	pyinstaller main.spec

dv:
	maturin develop --release

ds:
	python -m PyQt6.uic.pyuic design\MainWindow_UI.ui -o package\ui\mainwindow_ui.py
	python -m PyQt6.uic.pyuic design\ConfigDialog_UI.ui -o package\ui\configdialog_ui.py
	python -m PyQt6.uic.pyuic design\ErrorDialog_UI.ui -o package\ui\errordialog_ui.py
	python -m PyQt6.uic.pyuic design\OwnerDialog_UI.ui -o package\ui\ownerdialog_ui.py

env:
	.\.env\Scripts\activate.ps1
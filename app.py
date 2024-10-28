import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer, QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador Personalizado")

        # Inicializa a GUI e abas
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.new_tab)
        self.tabs.currentChanged.connect(self.update_url)
        self.setCentralWidget(self.tabs)

        # Botão para adicionar uma nova aba
        add_tab_button = QPushButton("+")
        add_tab_button.clicked.connect(lambda: self.add_new_tab("https://www.google.com"))
        self.tabs.setCornerWidget(add_tab_button)

        # Adiciona uma primeira aba
        self.add_new_tab("https://www.google.com")

        # Monitoramento de Sistema
        self.status_bar = QLabel()
        self.statusBar().addPermanentWidget(self.status_bar)
        self.update_system_info()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)  # Atualiza a cada segundo

    def add_new_tab(self, url):
        # Cria a nova aba com um layout que inclui um botão de fechar
        new_tab = QWidget()
        layout = QVBoxLayout()
        
        # Web Engine View
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        layout.addWidget(browser)

        # Botão de fechar aba
        close_button = QPushButton("Fechar aba")
        close_button.clicked.connect(lambda: self.close_tab(self.tabs.indexOf(new_tab)))
        layout.addWidget(close_button)

        new_tab.setLayout(layout)

        # Adiciona a aba ao TabWidget
        index = self.tabs.addTab(new_tab, url)
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        # Fecha a aba apenas se houver mais de uma aberta
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_system_info(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        if hasattr(psutil, 'sensors_temperatures'):
            gpu = psutil.sensors_temperatures().get('gpu', [None])[0].current if psutil.sensors_temperatures().get('gpu') else 'N/A'
        else:
            gpu = 'N/A'

        self.status_bar.setText(f"CPU: {cpu}% | RAM: {ram}% | GPU Temp: {gpu}°C")

    def update_url(self, index):
        current_browser = self.tabs.currentWidget().layout().itemAt(0).widget()
        if current_browser:
            url = current_browser.url().toString()
            print("URL atual:", url)

    def new_tab(self):
        self.add_new_tab("https://www.google.com")

app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())

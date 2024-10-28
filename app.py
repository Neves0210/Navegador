import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QTabBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer, QUrl, Qt

class SystemMonitor:
    @staticmethod
    def get_system_info():
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        gpu = SystemMonitor.get_gpu_temp()
        return f"CPU: {cpu}% | RAM: {ram}% "

    @staticmethod
    def get_gpu_temp():
        if hasattr(psutil, 'sensors_temperatures'):
            gpu_temp = psutil.sensors_temperatures().get('gpu', [None])[0]
            return f"{gpu_temp.current}°C" if gpu_temp else 'N/A'
        return 'N/A'


class TabManager(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.update_url)

        # Adiciona a primeira aba
        self.add_new_tab("https://www.google.com")

        # Adiciona o botão de nova aba como a última aba
        self.addTab(QWidget(), "+")
        self.tabBar().tabButton(self.count() - 1, QTabBar.RightSide).setDisabled(True)
        self.setTabEnabled(self.count() - 1, False)  # Desabilita a aba "+"

    def add_new_tab(self, url):
        new_tab = QWidget()
        layout = QVBoxLayout()
        browser = BrowserWidget(url)
        layout.addWidget(browser)
        new_tab.setLayout(layout)

        # Insere a nova aba antes da aba "+"
        index = self.insertTab(self.count() - 1, new_tab, "Nova Aba")
        self.setCurrentIndex(index)

    def close_tab(self, index):
        if self.count() > 2:  # Garante que ao menos uma aba e o botão "+" permaneçam
            self.removeTab(index)

    def update_url(self, index):
        current_widget = self.currentWidget()
        if current_widget and current_widget.layout():
            current_browser = current_widget.layout().itemAt(0).widget()
            if isinstance(current_browser, QWebEngineView):
                url = current_browser.url().toString()
                self.setTabText(index, url)

    def mousePressEvent(self, event):
        tab_index = self.tabBar().tabAt(event.pos())
        if tab_index == self.count() - 1:  # Verifica se clicou na aba "+"
            self.add_new_tab("https://www.google.com")
        else:
            super().mousePressEvent(event)  # Chama o método pai se não foi na aba "+"


class BrowserWidget(QWebEngineView):
    def __init__(self, url):
        super().__init__()
        self.setUrl(QUrl(url))
        self.loadFinished.connect(self.inject_js)

    def inject_js(self):
        js_code = """
            document.cookie = "session_id=valor_do_token; SameSite=None; Secure; HttpOnly";
            console.log(document.cookie);
        """
        self.page().runJavaScript(js_code)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador Neves")

        self.tabs = TabManager(self)
        self.setCentralWidget(self.tabs)

        self.status_bar = QLabel()
        self.statusBar().addPermanentWidget(self.status_bar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)
        self.update_system_info()

    def update_system_info(self):
        self.status_bar.setText(SystemMonitor.get_system_info())


app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())

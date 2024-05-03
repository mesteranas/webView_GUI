import sys
from custome_errors import *
sys.excepthook = my_excepthook
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtWebEngineWidgets import QWebEngineView
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.tabs=qt.QTabWidget()
        layout.addWidget(self.tabs)
        self.tabs.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.oncontext)
        qt1.QShortcut("ctrl+w",self).activated.connect(self.On_close_tab)
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        web=mb.addMenu("web")
        newTab=qt1.QAction(_("new tab"),self)
        web.addAction(newTab)
        newTab.triggered.connect(self.on_newTab)
        newTab.setShortcut("ctrl+n")
        refreshPage = qt1.QAction(_("Refresh Page"), self)
        web.addAction(refreshPage)
        refreshPage.triggered.connect(self.refresh_page)
        refreshPage.setShortcut("f5")
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def on_newTab(self):
        url,OK=qt.QInputDialog.getText(self,_("url"),_("type url"))
        if OK:
            widget=qt.QWidget()
            layout=qt.QVBoxLayout(widget)
            web=QWebEngineView()
            web.setUrl(qt2.QUrl(url))
            layout.addWidget(web)
            self.tabs.addTab(widget,web.title())
    def refresh_page(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            current_widget = self.tabs.widget(current_index)
            if isinstance(current_widget, qt.QWidget):
                layout = current_widget.layout()
                if layout is not None and layout.count() > 0:
                    web_view = layout.itemAt(0).widget()
                    if isinstance(web_view, QWebEngineView):
                        web_view.reload()
    def oncontext(self):
        menu=qt.QMenu(self)
        close=qt1.QAction(_("close page"),self)
        close.triggered.connect(self.On_close_tab)
        menu.addAction(close)
        menu.exec()
    def On_close_tab(self):
        self.tabs.removeTab(self.tabs.currentIndex())
App=qt.QApplication(sys.argv)
w=main()
w.show()
App.setStyle('fusion')
App.exec()
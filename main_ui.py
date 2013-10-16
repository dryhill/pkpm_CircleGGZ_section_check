# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyQt4.QtGui import QMainWindow

from Ui_main_ui import Ui_pkpm


class pkpmggz(QMainWindow, Ui_pkpm):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    ui = pkpmggz()

#显示界面
    ui.show()
#
    sys.exit(app.exec_())

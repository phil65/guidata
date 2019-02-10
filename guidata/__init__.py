# -*- coding: utf-8 -*-

__version__ = '1.7.5'


def qapplication():
    """
    Return QApplication instance
    Creates it if it doesn't already exist
    """
    from qtpy.QtWidgets import QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    install_translator(app)
    return app


QT_TRANSLATOR = None


def install_translator(qapp):
    """Install Qt translator to the QApplication instance"""
    global QT_TRANSLATOR
    if QT_TRANSLATOR is None:
        from qtpy.QtCore import QLocale, QTranslator, QLibraryInfo
        locale = QLocale.system().name()
        # Qt-specific translator
        qt_translator = QTranslator()
        paths = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
        if qt_translator.load("qt_" + locale, paths):
            QT_TRANSLATOR = qt_translator  # Keep reference alive
    if QT_TRANSLATOR is not None:
        qapp.installTranslator(QT_TRANSLATOR)

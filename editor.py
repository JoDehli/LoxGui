from PyQt5.Qsci import QsciLexerJSON
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor


class JSONEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lexer = QsciLexerJSON(self)
        # # Default text settings
        # self.lexer.setDefaultColor(QColor("#cccccc"))
        # self.lexer.setDefaultPaper(QColor("#cccccc"))
        # self.lexer.setDefaultFont(QFont("Consolas", 14))

        self.setLexer(QsciLexerJSON(self))
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(14)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

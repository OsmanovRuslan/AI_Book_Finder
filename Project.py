import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from mydesign import Ui_MainWindow
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec
import pandas as pd
import string
from nltk.tokenize import word_tokenize

data = pd.read_csv('books.csv')


class Book(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.start()
        self.checkin_completion = 0
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.ui.scrollAreaWidgetContents.setLayout(self.vbox)
        self.ui.scrollArea.verticalScrollBar().update()
        self.ui.textEdit.textChanged.connect(lambda: self.enter())
        self.stop_words = set(stopwords.words('russian'))
        print(self.stop_words)

    def start(self):
        self.ui.pushButton.clicked.connect(lambda: self.text_searche())

    def enter(self):
        if self.ui.textEdit.toPlainText() == "\n":
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Введите описание книги! ")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        elif "\n" in self.ui.textEdit.toPlainText():
            self.text_searche()

    def clearvbox(self, L=False):
        if not L:
            L = self.vbox
        if L is not None:
            while L.count():
                item = L.takeAt(0)

                widget = item.widget()

                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearvbox(item.layout())

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())

        # Удаление пунктуации и стоп-слов
        tokens = [word for word in tokens if word not in self.stop_words and word not in string.punctuation]

        return tokens

    def text_searche(self):
        model = Doc2Vec.load('doc2vec.model')
        try:
            self.clearvbox()
            query = self.ui.textEdit.toPlainText()
            self.ui.textEdit.setText("")
            query_vector = model.infer_vector(self.preprocess_text(query))
            similar_docs = model.dv.most_similar([query_vector], topn=10) # использует косинусное расстояние
            print(similar_docs)
            self.ui.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            for doc_id, sim_score in similar_docs:
                textPrecent = int(sim_score * 100)

                textlabel = data.iloc[doc_id]['title'] + "  (совпадение: " + str(textPrecent) + "%)"
                textlabel2 = data.iloc[doc_id]['description']
                label = QtWidgets.QLabel(textlabel)
                label.setMaximumWidth(460)
                label.setMinimumHeight(4)
                label.setStyleSheet('color: rgb(4, 53, 185); font: bold 18px;')
                label2 = QtWidgets.QLabel(textlabel2)
                label2.setStyleSheet('color: rgb(86, 111, 178); font: bold 13px;')
                label2.setMinimumHeight(60)
                label2.setMaximumWidth(460)
                label3 = QtWidgets.QLabel()
                label3.setMinimumHeight(8)
                if len(textlabel) >= 40:
                    label.setWordWrap(True)
                    label3.setWordWrap(True)
                if len(textlabel2) >= 40:
                    label2.setWordWrap(True)
                    label3.setWordWrap(True)

                self.vbox.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
                self.vbox.addWidget(label)
                self.vbox.addWidget(label2)
                self.vbox.addWidget(label3)
                self.vbox.update()

        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Что то пошло не так")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()


if __name__ == '__main__':
    app = QApplication([])
    application = Book()
    application.show()
    sys.exit(app.exec())

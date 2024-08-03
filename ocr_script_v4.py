import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextCharFormat
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Tesseract OCR'ın kurulu olduğu yolu belirt
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('OCR Görsel İşleme')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #333333;")
        
        layout = QVBoxLayout()

        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(QFont('Helvetica', 12))
        self.textEdit.setStyleSheet("background-color: black; color: lime;")
        layout.addWidget(self.textEdit)

        btn = QPushButton('Görselleri Seç', self)
        btn.setFont(QFont('Helvetica', 12))
        btn.setStyleSheet("background-color: #4CAF50; color: white;")
        btn.clicked.connect(self.showDialog)
        layout.addWidget(btn)

        self.setLayout(layout)

    def showDialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, 'Görselleri Seçin', '', 'Image Files (*.png *.jpg *.jpeg);;All Files (*)', options=options)
        if files:
            self.processImages(files)

    def processImages(self, files):
        for file in files:
            self.processImage(file)

    def processImage(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.convert('L')
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)
            image = image.filter(ImageFilter.SHARPEN)
            text = pytesseract.image_to_string(image, lang='eng')
            
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.End)
            
            # Kırmızı renk formatı oluştur
            red_format = QTextCharFormat()
            red_format.setForeground(QColor("red"))
            red_format.setFontWeight(QFont.Bold)
            red_format.setFontUnderline(True)
            red_format.setFontPointSize(14)  # Varsayılan font boyutunu 12 kabul ederek 2 artırma
            
            # Yeşil renk formatı oluştur
            green_format = QTextCharFormat()
            green_format.setForeground(QColor("lime"))
            
            # Kırmızı renkte dosya adı ekle
            cursor.insertText(f"{os.path.basename(image_path)}:\n", red_format)
            
            # Yeşil renkte metin ekle
            cursor.insertText(f"{text}\n\n", green_format)
        except Exception as e:
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.End)
            
            # Kırmızı renk formatı oluştur
            red_format = QTextCharFormat()
            red_format.setForeground(QColor("red"))
            red_format.setFontWeight(QFont.Bold)
            red_format.setFontUnderline(True)
            red_format.setFontPointSize(14)
            
            # Kırmızı renkte hata mesajı ekle
            cursor.insertText(f"Error processing {os.path.basename(image_path)}: {e}\n\n", red_format)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OCRApp()
    ex.show()
    sys.exit(app.exec_())
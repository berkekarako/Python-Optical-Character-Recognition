import os
import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Tesseract OCR'ın kurulu olduğu yolu belirt
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Metin dosyasının yolunu belirle
output_file = '/Users/berkekarakoc/Desktop/TEST/output.txt'

# Görseli işle ve metne dönüştür
def process_image(image_path, text_widget):
    try:
        image = Image.open(image_path)
        
        # Görseli gri tonlamalı yapma
        image = image.convert('L')
        
        # Kontrastı artırma
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        
        # Görseli biraz keskinleştirme
        image = image.filter(ImageFilter.SHARPEN)
        
        # OCR işlemi
        text = pytesseract.image_to_string(image, lang='eng')
        text_widget.insert(tk.END, f"{os.path.basename(image_path)}:\n{text}\n\n")
    except Exception as e:
        text_widget.insert(tk.END, f"Error processing {os.path.basename(image_path)}: {e}\n\n")

# Dosya seçme işlevi
def select_files():
    filetypes = (
        ('Image files', '*.png *.jpg *.jpeg'),
        ('All files', '*.*')
    )
    files = filedialog.askopenfilenames(title='Görselleri Seçin', filetypes=filetypes)
    for file in root.tk.splitlist(files):
        process_image(file, text_widget)

# GUI oluşturma
root = tk.Tk()
root.title("OCR Görsel İşleme")

# Pencereyi ayarlama
canvas = tk.Canvas(root, height=400, width=600, bg='white')
canvas.pack()

frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

label = tk.Label(frame, text="Görselleri seçmek için butona tıklayın", bg='white')
label.pack(pady=20)

button = tk.Button(frame, text="Görselleri Seç", padx=10, pady=5, fg="white", bg="black", command=select_files)
button.pack()

# Metin kutusu oluşturma
text_widget = Text(frame, wrap='word', bg='black')
text_widget.pack(pady=10, padx=10, fill='both', expand=True)

# GUI döngüsünü başlatma
root.mainloop()
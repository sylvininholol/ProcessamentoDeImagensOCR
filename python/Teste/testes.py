from filtros import *
from funcoes import *
import cv2
import pytesseract
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import re


pytesseract.pytesseract.tesseract_cmd = 'C:\Tesseract\Tesseract.exe'

img = cv2.imread("alogalera.jpg")
showImageGrid(img, "Função")





"""img = cv2.imread("tomcinza.jpg")
img = mediana(img)
localizar_texto_imagem(img)
img = cv2.imread("tomcinza.jpg")
img = redimensionar_imagem_para_tela(img)
img = gray(img)
img = blur(img, 2)
img = simple_threshold(img, 70)
cv2.imshow("Processada",img)
cv2.waitKey(0)
resultado = pytesseract.image_to_string(img)
print(resultado)"""

#img = reconhecer_caractere("mousepad.jpg")

#img = cv2.imread("mousepad.jpg")

#img = pre_processamento(img)

#cv2.imshow("Imagem Final", img)
#cv2.waitKey(0)

#cv2.imshow("Depois do processamento", img)
#cv2.waitKey(0)


#Pré-Processamento

#Impressões, Análises

#Pós-Processamento

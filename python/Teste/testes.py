from filtros import *
from funcoes import *
import cv2
import pytesseract
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import re


pytesseract.pytesseract.tesseract_cmd = 'C:\Tesseract\Tesseract.exe'




img = cv2.imread("fontedistorcida.jpg")
cv2.imshow("Original", img)
cv2.waitKey(0)                                  
img = mediana(img)                  
img = simple_threshold(img, 160)
img = ler_imagem(img)
pos_processamento(img)



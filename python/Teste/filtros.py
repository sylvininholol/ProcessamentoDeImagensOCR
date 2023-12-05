from funcoes import *
import cv2
import pytesseract
import numpy as np
import tkinter as tk
import re
from PIL import Image, ImageTk
import unicodedata
from matplotlib import pyplot as plt
import matplotlib
pytesseract.pytesseract.tesseract_cmd = 'C:\Tesseract\Tesseract.exe'


def gray(img_path):
    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    root.destroy()
    #img = cv2.imread(img_path)
    #img = cv2.resize(img_path, (largura_tela, altura_tela))
    #cv2.imshow('original image', img)
    #cv2.waitKey(0)
    gray = cv2.cvtColor(img_path, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    cv2.waitKey(0)
    return gray


def sharp(img):
    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    root.destroy()
    sharp1 = np.array([[0, -1, 0],
                    [-1,8, -1],
                    [0, -1, 0]])
         
    shrp = cv2.filter2D(img, -1, sharp1)
    #shrp = cv2.resize(shrp, (largura_tela, altura_tela))
    cv2.imshow('sharp', shrp)
    cv2.waitKey(0)
    return shrp


def simple_threshold(img_path, mim_threshold):
    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    root.destroy()
    val, thresh = cv2.threshold(img_path, mim_threshold, 255, cv2.THRESH_BINARY) #pixeis q forem inferiores a mim_threshold serão considerados como 0 e se for maior, sera considerado como 255(branco)
    #thresh = cv2.resize(thresh, (largura_tela, altura_tela))
    cv2.imshow('thresh', thresh)

    cv2.waitKey(0)

    return thresh



def mediana(img):
    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    root.destroy()
    mediana = cv2.medianBlur(img, 5)
    #mediana = cv2.resize(mediana, (largura_tela, altura_tela))
    cv2.imshow('mediana', mediana)
    cv2.waitKey(0)
    return mediana

class IdealNotchFilter:
    def __init__(self):
        pass
    
    def apply_filter(self, fshift, points, d0, path):
        m = fshift.shape[0]
        n = fshift.shape[1]
        for u in range(m):
            for v in range(n):
                for d in range(len(points)):
                    u0 = points[d][0]
                    v0 = points[d][1]
                    u0, v0 = v0, u0
                    d1 = pow(pow(u - u0, 2) + pow(v - v0, 2), 1)
                    d2 = pow(pow(u + u0, 2) + pow(v + v0, 2), 1)
                    if d1 <= d0 or d2 <= d0:
                        fshift[u][v] *= 0.0
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        matplotlib.image.imsave(path, img_back, cmap = "gray")
        return
    
class ButterworthNotchFilter:
    def __init__(self):
        pass
    
    def apply_filter(self, fshift, points, d0, path, order = 1):
        m = fshift.shape[0]
        n = fshift.shape[1]
        for u in range(m):
            for v in range(n):
                for d in range(len(points)):
                    u0 = points[d][0]
                    v0 = points[d][1]
                    u0, v0 = v0, u0
                    d1 = pow(pow(u - u0, 2) + pow(v - v0, 2), 0.5)
                    d2 = pow(pow(u + u0, 2) + pow(v + v0, 2), 0.5)
                    fshift[u][v] *= (1.0 / (1 + pow((d0 * d0) / (d1 * d2), order))) 
                    
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        matplotlib.image.imsave(path, img_back, cmap = "gray")
        return
    
class GaussianNotchFilter:
    def __init__(self):
        pass
    
    def apply_filter(self, fshift, points, d0, path):
        m = fshift.shape[0]
        n = fshift.shape[1]
        for u in range(m):
            for v in range(n):
                for d in range(len(points)):
                    u0 = points[d][0]
                    v0 = points[d][1]
                    u0, v0 = v0, u0
                    d1 = pow(pow(u - u0, 2) + pow(v - v0, 2), 0.5)
                    d2 = pow(pow(u + u0, 2) + pow(v + v0, 2), 0.5)
                    fshift[u][v] *= (1 - exp(-0.5 * (d1 * d2 / pow(d0, 2))))

        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        matplotlib.image.imsave(path, img_back, cmap = "gray")
        return
    
def blur(imagem_path, x):
    # Carregar a imagem original
    #imagem_original = cv2.imread(imagem_path)

    # Aplicar um desfoque médio (blur)
    imagem_com_blur = cv2.blur(imagem_path, (x, x), 0)  # O segundo argumento é o tamanho do kernel
    cv2.imshow("Blur", imagem_com_blur)
    cv2.waitKey(0)
    
    return imagem_com_blur


def filtro_destaque(imagem_path):
    # Carregar a imagem original
    #imagem_original = cv2.imread(imagem_path)

    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem_path, cv2.COLOR_BGR2GRAY)

    # Aplicar o filtro Laplaciano para realçar as bordas
    imagem_destacada = cv2.Laplacian(imagem_cinza, cv2.CV_64F)

    # Normalizar a imagem resultante para o intervalo [0, 255]
    imagem_destacada = cv2.normalize(imagem_destacada, None, 0, 255, cv2.NORM_MINMAX)

    # Converter de volta para o tipo de dados uint8
    imagem_destacada = np.uint8(imagem_destacada)

    # Combinação da imagem original com a imagem destacada para realçar as bordas
    imagem_resultante = cv2.addWeighted(imagem_path, 1, cv2.cvtColor(imagem_destacada, cv2.COLOR_GRAY2BGR), 0.25, 0)
    cv2.imshow("Imagem Realçada", imagem_resultante)
    cv2.waitKey(0)
    return imagem_resultante

def filtro_prewitt(imagem_path):
    # Carregar a imagem original
    #imagem_original = cv2.imread(imagem_path)

    # Converter a imagem para escala de cinza
    imagem_cinza1 = cv2.cvtColor(imagem_path, cv2.COLOR_BGR2GRAY)

    # Aplicar os filtros de Prewitt
    prewitt_x = cv2.filter2D(imagem_cinza1, cv2.CV_64F, np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]))
    prewitt_y = cv2.filter2D(imagem_cinza1, cv2.CV_64F, np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]))

    # Calcular a magnitude do gradiente
    magnitude_gradiente = np.sqrt(prewitt_x**2 + prewitt_y**2)

    # Normalizar a magnitude para o intervalo [0, 255]
    magnitude_gradiente = np.uint8(255 * magnitude_gradiente / np.max(magnitude_gradiente))
    img = magnitude_gradiente
    cv2.imshow("Prewitt", img)
    cv2.waitKey(0)
    return img


def binarizaracao(imagem_path):
    # Carregar a imagem original
    #imagem_original = cv2.imread(imagem_path)

    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem_path, cv2.COLOR_BGR2GRAY)

    # Aplicar a binarização de Otsu
    _, imagem_binaria = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img = imagem_binaria
    cv2.imshow("Binarizacao", imagem_binaria)
    cv2.waitKey(0)
    
    return imagem_binaria
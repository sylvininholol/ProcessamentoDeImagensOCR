import filtros
import cv2
import pytesseract
import numpy as np
import tkinter as tk
import re
from PIL import Image, ImageTk
import unicodedata
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = 'C:\Tesseract\Tesseract.exe'

def localizar_texto_imagem(imagem_path): #relativamente bom com os filtros necessários
    # Carregar a imagem
    #imagem = cv2.imread(imagem_path)

    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem_path, cv2.COLOR_BGR2GRAY)

    # Aplicar binarização para destacar o texto
    _, imagem_binaria = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)

    # Encontrar contornos na imagem binária
    contornos, _ = cv2.findContours(imagem_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterar sobre os contornos encontrados
    for contorno in contornos:
        # Calcular a caixa delimitadora do contorno
        x, y, w, h = cv2.boundingRect(contorno)

        # Desenhar um retângulo ao redor do contorno
        cv2.rectangle(imagem_path, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Exibir a imagem com os contornos destacados
    cv2.imshow('Contornos de Texto', imagem_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Exemplo de uso da função
#localizar_texto_imagem('caminho/para/sua/imagem.jpg')




def ler_imagem(imagem_path):
    # Carregar a imagem
    #imagem = cv2.imread(imagem_path)

    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem_path, cv2.COLOR_BGR2GRAY)

    # Aplicar binarização para destacar o texto
    _, imagem_binaria = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)


    # Reconhecimento de texto usando Tesseract
    texto_reconhecido = pytesseract.image_to_string(imagem_binaria, lang='por')  # 'por' para português

    # Exibir o texto reconhecido
    print("Texto Reconhecido:")
    print(texto_reconhecido)

# Exemplo de uso da função
#reconhecer_caractere('caminho/para/seu/caractere.jpg')

def pos_processamento(texto_reconhecido):
    # Remover acentos
    texto_sem_acentos = ''.join(c for c in unicodedata.normalize('NFD', texto_reconhecido) if unicodedata.category(c) != 'Mn')

    # Remover caracteres não alfanuméricos, pontos e vírgulas
    texto_limpo = re.sub(r'[^a-zA-Z0-9\s.,;]', '', texto_sem_acentos)

    # Remover espaços extras e quebras de linha
    texto_limpo = ' '.join(texto_limpo.split())
    
    return print(texto_limpo)

# Exemplo de uso
#texto_reconhecido = " E#xemp$lo de  text?o reco;nhe&cid#o."
#texto_pos_processado = pos_processamento(texto_reconhecido)
#print("Texto Pós-Processado:")
#print(texto_pos_processado)

def redimensionar_imagem_para_tela(imagem_path):
    # Obter as dimensões da tela
    root = tk.Tk()
    largura_tela = 750 #root.winfo_screenwidth()
    altura_tela = 750 #root.winfo_screenheight()
    root.destroy()

    # Carregar a imagem
    #imagem = cv2.imread(imagem_path)

    # Redimensionar a imagem para as dimensões da tela
    imagem_redimensionada = cv2.resize(imagem_path, (largura_tela, altura_tela))

    # Exibir a imagem redimensionada
    cv2.imshow('Imagem Redimensionada', imagem_redimensionada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return imagem_redimensionada

# Exemplo de uso da função
#redimensionar_imagem_para_tela('caminho/para/sua/imagem.jpg')

#Pré Processamento com redimensionalização de tela, filtro cinza, threshold, erosão e dilatação
def pre_processamento(img) -> cv2.typing.MatLike:
    kernel = np.ones((3,3),np.uint8)
    imagemPreProcessada = redimensionar_imagem_para_tela(img)
    
    #Deixar cinza
    imagemPreProcessada = filtros.gray(imagemPreProcessada)
    
    #Threshold
    imagemPreProcessada = filtros.simple_threshold(imagemPreProcessada, 127)
    
    #erosão
    imagemPreProcessada = cv2.erode(imagemPreProcessada, kernel, iterations=1)
    
    #dilatação
    imagemPreProcessada = cv2.dilate(imagemPreProcessada, kernel, iterations = 1)
    
    return imagemPreProcessada
    

def segmentar_caractere_texto(img):
    text = pytesseract.image_to_boxes(img)
    texto = [char for char in text if re.match('[a-zA-Z]', char)]

    print(texto)
    

def segmentar_caracteres_imagem(imagem_path):
    # Carregar a imagem original
    #imagem_original = cv2.imread(imagem_path)

    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem_path, cv2.COLOR_BGR2GRAY)

    # Aplicar binarização para destacar o texto
    _, imagem_binaria = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos na imagem binária
    contornos, _ = cv2.findContours(imagem_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extrair regiões de interesse (ROIs) dos contornos
    for i, contorno in enumerate(contornos):
        x, y, w, h = cv2.boundingRect(contorno)

        # Ignorar pequenos contornos (ajuste conforme necessário)
        if w > 10 and h > 10:
            # Extrair ROI da imagem original
            caractere_roi = imagem_path[y:y+h, x:x+w]

            cv2.imshow("Caractere Segmentado", caractere_roi)
            cv2.waitKey(0)
            
def showImage(img):
    imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(imgMPLIB)
    plt.show()

def showSingleImage(img, title, size):
    fig, axis = plt.subplots(figsize = size)

    axis.imshow(img, 'gray')
    axis.set_title(title, fontdict = {'fontsize': 22, 'fontweight': 'medium'})
    plt.show()
    
def showMultipleImages(imgsArray, titlesArray, size, x, y):
    if(x < 1 or y < 1):
        print("ERRO: X e Y não podem ser zero ou abaixo de zero!")
        return
    elif(x == 1 and y == 1):
        showSingleImage(imgsArray, titlesArray)
    elif(x == 1):
        fig, axis = plt.subplots(y, figsize = size)
        yId = 0
        for img in imgsArray:
            axis[yId].imshow(img, 'gray')
            axis[yId].set_anchor('NW')
            axis[yId].set_title(titlesArray[yId], fontdict = {'fontsize': 18, 'fontweight': 'medium'}, pad = 10)

            yId += 1
    elif(y == 1):
        fig, axis = plt.subplots(1, x, figsize = size)
        fig.suptitle(titlesArray)
        xId = 0
        for img in imgsArray:
            axis[xId].imshow(img, 'gray')
            axis[xId].set_anchor('NW')
            axis[xId].set_title(titlesArray[xId], fontdict = {'fontsize': 18, 'fontweight': 'medium'}, pad = 10)

            xId += 1
    else:
        fig, axis = plt.subplots(y, x, figsize = size)
        xId, yId, titleId = 0, 0, 0
        for img in imgsArray:
            axis[yId, xId].set_title(titlesArray[titleId], fontdict = {'fontsize': 18, 'fontweight': 'medium'}, pad = 10)
            axis[yId, xId].set_anchor('NW')
            axis[yId, xId].imshow(img, 'gray')
            if(len(titlesArray[titleId]) == 0):
                axis[yId, xId].axis('off')

            titleId += 1
            xId += 1
            if xId == x:
                xId = 0
                yId += 1
    plt.show()
    
def showImageGrid(img, title):
    fig, axis = plt.subplots()
    imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    axis.imshow(imgMPLIB)
    axis.set_title(title)
    plt.show()
    
def plotTwoImageHorizontal(img):
    
    imgOriginal = cv2.imread(img)
    imgReplicate = cv2.medianBlur(imgOriginal, 5)

    imgsArray = [imgOriginal, imgReplicate]
    titlesArray = ['Original', 'Filtro de Mediana']
    showMultipleImages(imgsArray, titlesArray, (12, 8), 2, 1)

    config = "--psm 4"
    resultado = pytesseract.image_to_string(imgReplicate, config=config)
    #criando grid com 2 imagens, a segunda com borda replicada
    imgsArray = [imgOriginal, imgReplicate]
    title = 'Imagem Original e Imagem com Adaptive Threshold'
    showMultipleImages(imgsArray, title, 2, 1)
    
def showSingleImage(img, title, size):
    fig, axis = plt.subplots(figsize = size)

    axis.imshow(img, 'gray')
    axis.set_title(title, fontdict = {'fontsize': 22, 'fontweight': 'medium'})
    plt.show()
    
def plotThreeImages():
    img_j_original = cv2.imread("trio.jpg", 0)

    #mesma imagem com erosão
        
    erosao =  cv2.erode(img_j_original, kernel, iterations=1)

    #imagem anterior com dilatação aplicada
    dilatacao =  cv2.dilate(erosao, kernel, iterations=1)

    imgsArray = [img_j_original, erosao, dilatacao]
    titlesArray = ['Imagem Original', 'Erosão', 'Dilatação']
    showMultipleImages(imgsArray, titlesArray, (10, 6), 3, 1)
    
    config = "--psm 4"
    resultado = pytesseract.image_to_string(dilatacao, config=config, lang='por')
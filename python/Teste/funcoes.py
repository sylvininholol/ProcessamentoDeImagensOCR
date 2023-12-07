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



    # Usar o Tesseract para extrair caixas delimitadoras do texto na imagem
def localizar_texto_imagem(imagem_path): #relativamente bom com os filtros necessários
    boxes = pytesseract.image_to_boxes(imagem_path)

    # Desenhar retângulos ao redor do texto na imagem original
    for box in boxes.splitlines():
        b = box.split()
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(imagem_path, (x, y), (w, h), (255, 0, 255), 2)

    # Exibir a imagem com os retângulos marcados
    cv2.imshow("Localized Text", imagem_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Exemplo de uso da função
#localizar_texto_imagem('caminho/para/sua/imagem.jpg')




def ler_imagem(imagem_path):

    imagem_binaria = pre_processamento(imagem_path)

    # Reconhecimento de texto usando Tesseract
    texto_reconhecido = pytesseract.image_to_string(imagem_binaria, lang='por')  # 'por' para português

    # Exibir o texto reconhecido
    print("Texto Reconhecido:")
    print(texto_reconhecido)
    return imagem_binaria

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


def redimensionar_imagem_para_tela(imagem_path):
    # Obter as dimensões da tela
    root = tk.Tk()
    largura_tela = 750 #root.winfo_screenwidth()
    altura_tela = 750 #root.winfo_screenheight()
    root.destroy()


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
    kernel = np.ones((2,2),np.uint8)
    imagemPreProcessada = redimensionar_imagem_para_tela(img)
    
    #Deixar cinza
    imagemPreProcessada = filtros.gray(imagemPreProcessada)
    
    imagemPreProcessada = filtros.filtro_destaque(imagemPreProcessada)
    #Threshold
    imagemPreProcessada = filtros.simple_threshold(imagemPreProcessada, 150)
    
    imagemPreProcessada = filtros.media(imagemPreProcessada, 3)
    #erosão
    imagemPreProcessada = cv2.erode(imagemPreProcessada, kernel, iterations=1)
    cv2.imshow("Erosao", imagemPreProcessada)
    cv2.waitKey(0)
    
    #dilatação
    imagemPreProcessada = cv2.dilate(imagemPreProcessada, kernel, iterations = 1)
    cv2.imshow("Dilatacao", imagemPreProcessada)
    cv2.waitKey(0)
    return imagemPreProcessada
    

def segmentar_caractere_texto(img):
    text = pytesseract.image_to_boxes(img)
    texto = [char for char in text if re.match('[a-zA-Z]', char)]

    print(texto)
    

def segmentar_caracteres_imagem(image_path):


    # Extrair caixas delimitadoras do texto na imagem
    boxes = pytesseract.image_to_boxes(image_path)

    # Iterar sobre as caixas delimitadoras e segmentar os caracteres
    for box in boxes.splitlines():
        b = box.split()
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

        # Extrair a região de interesse (ROI) correspondente a cada caractere
        character_roi = image_path[y:h, x:w]

        # Exibir cada caractere segmentado
        cv2.imshow("Segmented Character", character_roi)
        cv2.waitKey(0)  # Aguardar 1 segundo entre cada caractere
        cv2.destroyAllWindows()
            
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
    
def plotThreeImages(img):
        
    erosao =  cv2.erode(img, None, iterations=1)

    #imagem anterior com dilatação aplicada
    dilatacao =  cv2.dilate(erosao, None, iterations=1)

    imgsArray = [img, erosao, dilatacao]
    titlesArray = ['Imagem Original', 'Erosão', 'Dilatação']
    showMultipleImages(imgsArray, titlesArray, (10, 6), 3, 1)
    
    config = "--psm 4"
    resultado = pytesseract.image_to_string(dilatacao, config=config, lang='por')
    
def inverter_180_graus(imagem_path):


    # Inverte a imagem em 180 graus
    imagem_invertida = cv2.rotate(imagem_path, cv2.ROTATE_180)
    cv2.imshow("Invertida", imagem_invertida)
    cv2.waitKey(0)

    # Salva a imagem invertida
    return imagem_invertida

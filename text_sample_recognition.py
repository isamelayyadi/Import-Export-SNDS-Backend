# import the libraries

import pytesseract
import cv2
import re

"""
Ce module extracte tout le texte structuré présent sur une image
En entrée il prend une image et en sortie le texte extracté
"""

def text_sample_recognition(image,pytesseractexe):
    #The path of tesseract exe
    pytesseract.pytesseract.tesseract_cmd = pytesseractexe

    # loading the image from the disk
    image_to_ocr = image

    # preprocessing the image
    # step 1 : covert to grey scale
    preprocessed_img = cv2.cvtColor(image_to_ocr, cv2.COLOR_BGR2GRAY)

    # step2:Do binary and otsu thresholding
    #preprocessed_img = cv2.threshold(preprocessed_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # step 3 : Smooth the image using median blur
    #preprocessed_img = cv2.medianBlur(preprocessed_img, 3)

    # le choix des paramètres d'entrées de pytesseact, par défault eng et 7 pour structuré
    config = ("-l eng --oem 3 --psm 7")

    # pass the  image to tesseract to do OCR
    text_extracted = pytesseract.image_to_string(preprocessed_img,config=config)
    text_extracted=re.sub('[^a-zA-Z0-9 \n\.]', '', text_extracted)
    return text_extracted

#To test this module
#image= cv2.imread("images/test_ocr_1.jpg")
#print(text_sample_recognition(image))
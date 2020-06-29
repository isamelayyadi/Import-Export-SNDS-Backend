# import the libraries
from PIL import Image
import pytesseract
import cv2
import codecs
import re


def text_sample_recognition(image_name):


    path = "images/" + image_name
    # declaring the exe path for tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # loading the image from the disk
    image_to_ocr = cv2.imread(path)

    # preprocessing the image
    # step 1 : covert to grey scale
    preprocessed_img = cv2.cvtColor(image_to_ocr, cv2.COLOR_BGR2GRAY)

    # step2:Do binary and otsu thresholding
    #preprocessed_img = cv2.threshold(preprocessed_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # step 3 : Smooth the image using median blur
    #preprocessed_img = cv2.medianBlur(preprocessed_img, 3)

    # etape pour vérifier la qualité de l'image traitée
    cv2.imwrite('temp_img.jpg', preprocessed_img)

    preprocessed_pil_img = Image.open('temp_img.jpg')

    # le choix des paramètres d'entrées de pytesseact, par défault eng et 7 pour structuré
    # config = ("-l eng --oem 3 --psm 7")

    # pass the pil image to tesseract to do OCR
    text_extracted = pytesseract.image_to_string(preprocessed_img)

    # print the text
#    print(text_extracted)
    # Bricolage ....... A enlever
    regexp = r'(?=([\d]{15}))'
    regexp2 = r'(?=([A-Z0-9]{9}))'

    text = re.findall(regexp, text_extracted, re.DOTALL)



    text.append(re.findall(regexp2, text_extracted, re.DOTALL))
    print(text)
    print(len(text))
    print(text[0])
    if text[0] != [] :
    #print('il y a un num de sécurité!:', text)
        return {"text": text_extracted, "num": text, "controle": "ko"}

    else:
        return {"text" : text_extracted, "num": "noNum", "controle" : "ok"}

    #Fichier de sortie :
    file = codecs.open("result.txt", "w", "utf-8")
    file.write(text)

    # display the original image
    cv2.imshow("Actual Image", image_to_ocr)

    #Retour d'un dictionnaire {text , num, controle}




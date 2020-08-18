from size_object import size_object
from text_sample_recognition import text_sample_recognition
from detection_text_image import detection_text_image
from text_recognition_image import text_recognition_image
from control_stegano_exif import  control_stegano, extension
from control_file_ps import open_file_ps
from control_text_file_regex import control_regex
import cv2
import numpy
from PIL import Image


path = "images/test_ocr_6.jpg"
path = "images/Fichiers PS/02_age_sexe.ps"
path = "images/test_ocr_10.jpg"
path="images/Fichiers IMG/KO/test_gif_ko.gif"
"""
Initialisation des paramètres :
"""

# Path of east
east = "east_text_detection.pb"
# le path de l'exe de tesseract
pytesseractexe = r'C:\Users\i.el-ayyadi-la\Tesseract-OCR\tesseract.exe'
# padding initial
# min_confidence , par defaul : 0,5
padding = 0.1
min_confidence = 0.5
# resize, par default
(height, width) = (320, 320)
# size of object :
# size of object par default
widthO = 1
# dictionnaire des listes des contrôles
results = {}


def main():
    all_text = []
    test_objet_gif=0
    """
    Contôle stegano et determination de l'extention de l'image :
    """
    extension_image = extension(path)
    warning = control_stegano(path)
    """
    Cas 1 : Image PS
    """
    print(extension_image)
    if extension_image == "EPS":
        all_text.append(open_file_ps(path))

    """
       Cas 2 : Image PNG, JPG et TIFF
    """
    if extension_image in ["PNG", "JPG", "TIFF"]:


        image_name = cv2.imread(path)
        #test_objet : Object si il y a des objets, noObject sinon
        test_objet = size_object(image_name, widthO)

        if test_objet == "noObject":
            text_in_image ="text"
            all_text.append(text_sample_recognition(image_name, pytesseractexe))
        else:

            text_in_image = detection_text_image(image_name, east, min_confidence, width, height)
            if text_in_image == "text":
                all_text.append(
                    text_recognition_image(image_name, east, padding, min_confidence, width, height, pytesseractexe))

    """
       Cas 3 : Image GIF
    """
    if extension_image == "GIF":
        image = Image.open(path)
        frames = []
        for frame in range(image.n_frames):
            image.seek(frame)

            frame = numpy.asarray(image.convert('RGB'))
            frame = frame[:, :, ::-1].copy()
            frames.append(frame)
        for i in range(len(frames)):
            cv2.imshow("frame" + str(i + 1), frames[i])
            cv2.waitKey(100)
            image_name = frames[i]
            test_objet = size_object(image_name, widthO)

            if test_objet == "noObject":
                text_in_image_gif = "text"
                all_text.append(text_sample_recognition(image_name, pytesseractexe))
            else:

                test_objet_gif+=1
                text_in_image = detection_text_image(image_name, east, min_confidence, width, height)
                if text_in_image == "text":
                    all_text.append(
                        text_recognition_image(image_name, east, padding, min_confidence, width, height,
                                               pytesseractexe))

    text_results = "".join(all_text)
    num1,num2 = control_regex(text_results)
    if extension_image =="GIF" :
        if len(num1) == 0 and len(num2) == 0:
            results.update({"Extension" :extension_image,"Image_count":len(frames),
                            "Object": test_objet_gif, "text": text_in_image_gif,
                            "Num": "Nonum", "control": "ok"})

        else :
            results.update({"Extension" :extension_image,"Image_count":len(frames),
                            "Object": test_objet_gif, "text": text_in_image,
                            "Num": "  ".join(num1 + num2), "Number_Num": len(num1) + len(num2), "control": "ko"})
    else :
        if len(num1)==0 and len(num2)==0 :
            results.update({"Object": test_objet, "text": text_in_image, "Num": "Nonum", "control" : "ok"})

        else :
            results.update({"Object": test_objet, "text": text_in_image,
                            "Num": "  ".join(num1 + num2),"Number_Num" : len(num1)+len(num2),"control" :"ko"})

    print(results)



if __name__ == "__main__":
    main()

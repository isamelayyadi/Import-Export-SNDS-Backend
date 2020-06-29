from size_object import size_object
from text_sample_recognition import text_sample_recognition
from detection_text_image import detection_text_image
from text_recognition_image import text_recognition_image


image_name = "Capture_OK_donneesagregees.jpg"

# Path of east
east = "east_text_detection.pb"
# padding initial

# A ne pas changer ces parametres :
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
    print(size_object(image_name, widthO)["test_objet"])
    if size_object(image_name, widthO)["test_objet"] == "noObject":
        results.update(size_object(image_name, widthO))
        results.update(text_sample_recognition(image_name))


    else:
        results.update(size_object(image_name, widthO))
        if detection_text_image(image_name, east, min_confidence, width, height)["text"] == "notext":
            results.update(detection_text_image(image_name, east, min_confidence, width, height))

        else:
            results["text"] = "text"
            results.update(text_recognition_image(image_name, east, padding, min_confidence, width, height))

    print(results)


if __name__ == "__main__":
    main()

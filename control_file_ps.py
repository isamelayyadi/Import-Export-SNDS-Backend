import codecs



def open_file_ps(path):
    text = set()

    # Text extraction
    for line in open(path):

        for p in line.replace('\\(', 'EscapeLP').replace('\\)', 'EscapeRP').split('(')[1:]:
            text.add(codecs.decode(p[:p.find(')')].replace('EscapeLP', '(').replace('EscapeRP', ')'), 'unicode_escape'))
    # Find warning in exctract text
        text_result = " ".join(text)
    return text_result

#To test this module
#image1 = "images/Fichiers PS/01_Eff_liberaux.ps"
#image2 = "images/Fichiers PS/02_age_sexe.ps"
#print(open_file_eps(image2))

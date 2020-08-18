import re

def control_regex (text) :

    # regex pour le num de sécurité sociale
    # regex2 pour le NIR
    regexp = r'(?=([\d O o]{15}))'
    regexp2 = r'(?=([A-Z0-9]{11}))'

    num1 = re.findall(regexp, text.replace(" ", "").replace(".", ""), re.DOTALL)
    num2= re.findall(regexp2, text.replace(" ", "").replace(".", ""), re.DOTALL)

    return num1,num2
import subprocess
import os
import json


class ExifTool(object):
    sentinel = "{ready}\r\n"

    # path of exiftool exe
    def __init__(self, executable="exiftool.exe"):
        self.executable = executable

    #
    def __enter__(self):
        self.process = subprocess.Popen(
            [self.executable, "-stay_open", "True", "-@", "-"],
            universal_newlines=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()

    def execute(self, *args):
        args = args + ("-execute\n",)
        self.process.stdin.write(str.join("\n", args))
        self.process.stdin.flush()
        output = ""
        fd = self.process.stdout.fileno()
        # Pour Python 3, on doit décoder la série d'octets retournée par os.read()
        while not output.endswith(self.sentinel):
            output += os.read(fd, 4096).decode('utf-8')
        return output[:-len(self.sentinel)]

    # On génère un json de metadatas, pour plus d'option sur .exe voire : https://exiftool.org/

    def get_metadata(self, *filenames):
        return json.loads(self.execute("-G", "-j", "-n", *filenames))


def metadatas(filename):
    with ExifTool() as e:
        metadata = e.get_metadata(filename)
    return metadata

def extension (filename) :
    with ExifTool() as e:
        metadata = e.get_metadata(filename)

    return metadata[0]["File:FileTypeExtension"]
def control_stegano(image):

    warning = []
    for key, value in metadatas(image)[0].items():
        if "WARNING" in str(key).upper():
            warning.append(value)
        if len(str(value)) > 255 and "type=\"Seq" in value:
            warning.append(value)
    return warning


#To test this module
#image1 = "images\Fichiers IMG\KO\Capture_v5.jpeg"
#image2 = "images\Fichiers IMG\KO\Capture_v2.png"
#image3 = "images\Fichiers IMG\KO/nir_png.png"

#print("Warning Control Stegano: {}".format(control_stegano(image3)))
#print(extention(image3))
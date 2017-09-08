import sys
from subprocess import Popen, PIPE
import os
import tempfile
import cv2

PROG_NAME = 'tesseract'
TEMP_IMAGE = tempfile.mktemp()+'.bmp'
TEMP_FILE = tempfile.mktemp()

#All the PSM arguments as a variable name (avoid having to know them)
PSM_OSD_ONLY = 0
PSM_SEG_AND_OSD = 1
PSM_SEG_ONLY = 2
PSM_AUTO = 3
PSM_SINGLE_COLUMN = 4
PSM_VERTICAL_ALIGN = 5
PSM_UNIFORM_BLOCK = 6
PSM_SINGLE_LINE = 7
PSM_SINGLE_WORD = 8
PSM_SINGLE_WORD_CIRCLE = 9
PSM_SINGLE_CHAR = 10

class TesseractException(Exception): #Raised when tesseract does not return 0
    pass

class TesseractNotFound(Exception): #When tesseract is not found in the path
    pass

def check_path(): #Check if tesseract is in the path raise TesseractNotFound otherwise
    for path in os.environ.get('PATH', '').split(':'):
        filepath = os.path.join(path, PROG_NAME)
        if os.path.exists(filepath) and not os.path.isdir(filepath):
            return True
    raise TesseractNotFound()

def process_request(input_file, output_file, lang=None, psm=None):
    args = [PROG_NAME, input_file, output_file] #Create the arguments
    if lang is not None:
        args.append("-l")
        args.append(lang)
    if psm is not None:
        args.append("-psm")
        args.append(str(psm))
    proc = Popen(args, stdout=PIPE, stderr=PIPE) #Open process
    ret = proc.communicate() #Launch it

    code = proc.returncode
    if code != 0:
        if code == 2:
            raise TesseractException("File not found")
        if code == -11:
            raise TesseractException("Language code invalid: "+ret[1])
        else:
            raise TesseractException(ret[1])

def image_to_string(im, lang=None, psm=None):
    grayscale_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(TEMP_IMAGE, grayscale_image)
    txt = image_file_to_string(TEMP_IMAGE, lang, psm)
    os.remove(TEMP_IMAGE)
    return txt

def image_file_to_string(file, lang=None, psm=None):
    check_path() #Check if tesseract available in the path
    grayscale_image = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
    cv2.imwrite(TEMP_IMAGE, grayscale_image)
    #process_request(file, TEMP_FILE, lang, psm)
    process_request(TEMP_IMAGE, TEMP_FILE, lang, psm)
    f = open(TEMP_FILE+".txt", "r") #Open back the file
    txt = f.read()
    f.close()
    os.remove(TEMP_FILE+".txt")
    os.remove(TEMP_IMAGE)
    return txt


if __name__ =='__main__':
    print(image_file_to_string(sys.argv[2], sys.argv[1], PSM_AUTO))

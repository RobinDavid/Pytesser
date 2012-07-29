Pytesser
========

Python wrapper for the tesseract OCR engine. The module is based on OpenCV.
Article : http://robindavid.comli.com/pytesser-python-wrapper-for-the-tesseract-ocr-engine/

Informations
------------

There is already multiples module called pytesser, but this one is slightly different on the following point:

* It implement all the features of tesseract engine it includes the choise of the language and the page segmentation mode.
* All the module is contained in one file (the others modules I have tried are quite messy.
* It support OpenCV, so you can directly provide an IplImage to the module.

How to use it ?
---------------

There is to ways to use it. Either you give it a filename, either directly an IplImage. For a filename you can do:

    import pytesser
    txt = pytesser.image_to_string("myimage.jpg") #By default language is eng, and page seg mode auto

    #To give specifify parameters:
    txt = pytesser.image_to_string("myimage.jpg","fra",pytesser.PSM_SINGLE_WORD) #Analyse image as a single french word


Or you can directly give it an IplImage like this:

    image = cv.LoadImage("myimage.jpg")
    txt = pytesser.iplimage_to_string(image) 
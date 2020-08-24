import requests
import json
import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter


def ocr_space_file(filename,outputfile,api_key ,overlay=False,  language='eng' ):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
        :param filename: Your file path & name.
        :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
        :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    m = r.content.decode()
    jsonstr = json.loads(m)
    sys.stdout = open(outputfile, 'a+')
    print(jsonstr["ParsedResults"][0]["ParsedText"])


def pdf_splitter(path,outputfile,api_key):
    fname = os.path.splitext(os.path.basename(path))[0]
    print("filenameeeeeeeeeeee:",outputfile)

    pdf = PdfFileReader(path)
    content = ""
    dir=path[0:path.rfind("\\")]

    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = '{}_page_{}.pdf'.format(
            fname, page + 1)
        output_filename = dir+"\\"+output_filename
        print(dir)

        print(output_filename)


        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        # Calling the function
        #ocr_space_file(output_filename,outputfile,api_key, language='eng' )
        payload = {'isOverlayRequired': False,
                   'apikey': api_key,
                   'language': 'eng',
                   }
        with open(output_filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={output_filename: f},
                              data=payload,
                              )
        m = r.content.decode()
        jsonstr = json.loads(m)
        print(jsonstr["ParsedResults"][0]["ParsedText"])
        content = content+"\n"+jsonstr["ParsedResults"][0]["ParsedText"]

        # printing the names of two files created from pdf
        # print('Created: {}'.format(output_filename))
    #sys.stdout = open(outputfile, 'a+')
    with open(outputfile, "w+") as filewriter:
        print("reach here in conversion")
        filewriter.write(content)


if __name__ == '__main__':
    # Enter the path of your file here
    path = 'C:\\Users\\sanam\\Desktop\\AttomusFiles\\Erastamise_leping_EV.pdf'
    outputfile = "C:\\Users\\sanam\\Desktop\\AttomusFiles\\Erastamise_leping_EV.txt"
    api_key = "ceb870644788957"

    pdf_splitter(path,outputfile,api_key)

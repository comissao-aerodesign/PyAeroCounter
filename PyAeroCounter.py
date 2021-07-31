from pdfminer3.layout import LAParams, LTChar
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfpage import PDFPage
from pdfminer3.layout import LTTextBoxHorizontal, LAParams, LTTextBox, LTTextLine, LTFigure, LTTextLineHorizontal, LTImage
# get pdfminer3 in the following link: 
# #https://pypi.org/project/pdfminer3/

from binascii import b2a_hex
from copy import deepcopy
import getopt, sys
import os
import string
import io
import unicodedata

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

#  Get pytesseract and teressact:
#  https://pypi.org/project/pytesseract/
#  https://github.com/tesseract-ocr/tesseract   (windows - precompiled binaries: https://digi.bib.uni-mannheim.de/tesseract/)
#  tutorials: 
#     https://nanonets.com/blog/ocr-with-tesseract/  
#     https://stackabuse.com/pytesseract-simple-python-optical-character-recognition/

# ------------------------------

# In addition to the above libraries, the user must have the following software installed:
# Extract images from PDF using pdftohtml (miktex)
# Download:
# https://miktex.org/download
# https://miktex.org/packages/miktex-poppler-bin-2.9/files
# Installed file example: C:\Program Files\MiKTeX 2.9\miktex\bin\x64\pdftohtml.exe


# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Auxiliar functions

def parse_layout(string_from_LTFigure,layout):
    """Function to recursively parse the layout tree."""
    previous_line = 0
    for lt_obj in layout:        
        if isinstance(lt_obj, LTFigure):
            string_from_LTFigure = string_from_LTFigure + parse_layout(string_from_LTFigure,lt_obj)  # Recursive
        elif isinstance(lt_obj, LTChar) or isinstance(element, LTTextBoxHorizontal) or isinstance(element, LTTextBox) or isinstance(element, LTTextLine):
            if not previous_line == lt_obj.bbox[3]:
                string_from_LTFigure = string_from_LTFigure + ' '
                previous_line = lt_obj.bbox[3]
            string_from_LTFigure = string_from_LTFigure + lt_obj.get_text() 
    return string_from_LTFigure

def ocr_core(filename_extract):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename_extract))  
    return text

def usage():
    print(f'usage: [-o logfile] [-w wordsfile] [-n nonwordsfile] '
        ' [-d output_dir]  [-i input.pdf] [-e extract_words_from_images] [-f file_strings_from_images] [-g mathmodewords] ...')
    return 100

def return_categorized_words(words,countwords,countnonwords,count_mathwords):
    # This function select valid words that are considered in the final count
    # and separate them form the non-words items.
    # All the relevant criteria for word counting are applied in this function.
    count_mathwords = 0
    i = 0
    non_words = []
    while i<len(words):
        words_unicode = words[i].encode('raw_unicode_escape')

        # remove mathematical strings  (Microsoft Word)
        if 'U0001d' in str(words_unicode):
            
            # Counting words written in math mode (Microsoft Word)
            it_is_word = 0
            temp = deepcopy(str(words_unicode))
            temp = temp.replace("b'",'')
            temp = temp.split('\\')
            
            # remove empty items
            while '' in temp:
                temp.remove('') 

            for g in range(len(words[i])):
                if unicodedata.category(words[i][g]) in 'LuLl' and  len(temp)==len(words[i]) and len(temp[g])>7 and temp[g][7] in '0123456789':
                    it_is_word = 1
                elif unicodedata.category(words[i][g]) in 'Mn':
                    it_is_word = 1
                else:
                    it_is_word = 0
                    break

            if it_is_word:
                count_mathwords = count_mathwords+1
                if mathmodewords:
                    with io.open(mathmodewords,'a', encoding='utf8') as wfile:
                        wfile.write('{} '.format(words[i]))
                        wfile.write('\n')

            non_words.append(words[i])
            words.remove(words[i])
            countnonwords = countnonwords + 1
        # remove greek char
        elif '\\u03' in str(words_unicode):
            non_words.append(words[i])
            words.remove(words[i])
            countnonwords = countnonwords + 1
        # remove numeric strings 
        elif words[i].isnumeric() or any(punct in words[i] for punct in string.digits):
            non_words.append(words[i])
            words.remove(words[i])
            countnonwords = countnonwords + 1
        elif not words[i].isalpha() and not any(char in string.punctuation+'´¸˜-ˆ' for char in words[i]):
            non_words.append(words[i])
            words.remove(words[i])
            countnonwords = countnonwords + 1
        elif len(words[i]) == 1 and any(punct in words[i] for punct in string.punctuation):   
            non_words.append(words[i])
            words.remove(words[i])
            countnonwords = countnonwords + 1
        elif words[i] == len(words[i]) * '.':
            non_words.append(words[i])
            words.remove(words[i])
        else:
            i=i+1
            countwords = countwords+1

    return words, countwords, non_words, countnonwords, count_mathwords    

try:
    opts, args = getopt.getopt(sys.argv[1:],'o:w:n:d:i:e:f:g:')
except getopt.GetoptError as err:
    # print help information and exit:
    print(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

# default inputs
logfile = 'logfile.txt'
wordsfile = 'wordsfile.txt'
nonwordsfile = 'nonwordsfile.txt'
images_folder = 'PDFFILE'
pdffile = 'pdffile.pdf'
extract = 1
strings_figures = 'file_strings_from_images.txt'
mathmodewords = 'mathmodewords.txt'

# read inputs from user - command line
for (k, v) in opts:
    if k == '-o': logfile = v
    elif k == '-w': wordsfile = v
    elif k == '-n': nonwordsfile = v
    elif k == '-d': images_folder = v
    elif k == '-i': pdffile = v
    elif k == '-e': extract = v
    elif k == '-f': strings_figures = v
    elif k == '-g': mathmodewords = v


# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------
# PDFminer - count number of words

document = open(pdffile, 'rb')

#Create resource manager
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)


j = 0
counttext    = []
notcounttext = []
keywords = ['Lista de Símbolos','LISTA DE SIMBOLOS','Sumário','Lista de Inputs','Lista de Outputs','Bibliografia','Referências Bibliográﬁcas','Referências','References','Symbol List','Summary','Symbols and Acronyms','Inputs','Outputs','List of Inputs','List of Outputs','Bibliography']

countwords = 0
countnonwords = 0
countfigures = 0
count_mathwords = 0

count_specialpages = 0

if mathmodewords:
    with io.open(mathmodewords,'w', encoding='utf8') as wfile:
        wfile.write('\n')

for page in PDFPage.get_pages(document):
    j = j+1
    countpage = True
    # remove first page
    if j<=1:
        countpage = False
        count_specialpages = count_specialpages + 1

    interpreter.process_page(page)

    # receive the LTPage object for the page.
    layout = device.get_result()
    k = 0

    counttext.append([])
    notcounttext.append([])

    for element in layout:
        headerfooter = False
        position = element.bbox        
        if position[3]/28.35>=27.0 or position[1]/28.35<=1.75:
            headerfooter = True
        
        if isinstance(element, LTImage) or isinstance(element, LTFigure):
            countfigures = countfigures + 1
        
        string_from_LTFigure = ''
        if isinstance(element, LTFigure):            
            string_from_LTFigure = parse_layout(string_from_LTFigure,element)

        parse_element = 0

        if isinstance(element, LTTextBoxHorizontal) or isinstance(element, LTTextBox) or isinstance(element, LTTextLine) or len(string_from_LTFigure)>0:
            parse_element = 1
        
        if parse_element:            
            # get line text
            k = k+1
            if len(string_from_LTFigure)>0:
                words = string_from_LTFigure[:]
            else:
                words = element.get_text() 

            # check if the page must be considered
            if headerfooter and countpage:
                # remove breaklines
                words = words.replace('\n','')
                for keyword in keywords:
                    if keyword.lower() in words.lower():
                        countpage = False
                        count_specialpages = count_specialpages + 1
                        break
            
            # remove breaklines
            words = words.replace('\n',' ')

            # split line in words
            words = words.split(' ')            

            # remove empty items
            while '' in words:
                words.remove('') 

            # count only pages with valid content    
            if countpage and not headerfooter:
                words, countwords, non_words, countnonwords, count_mathwords = return_categorized_words(words,countwords,countnonwords,count_mathwords)
                
                # saving only words
                if len(words) > 0:
                    counttext[j-1].append(words)

                # saving only non-words
                if len(non_words) > 0:
                    notcounttext[j-1].append(non_words)
            else:
                notcounttext[j-1].append(words)

number_of_pages = j
countwords_text = countwords
countnonwords_text = countnonwords

countwords = 0
countnonwords = 0

countfigures_pdfminer = countfigures
countfigures = 0

# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Extract images from PDF using pdftohtml (miktex)
# Download:
# https://miktex.org/download
# https://miktex.org/packages/miktex-poppler-bin-2.9/files
# Installed file example: C:\Program Files\MiKTeX 2.9\miktex\bin\x64\pdftohtml.exe

if images_folder:
    os.system('pdftohtml -q -zoom 1 ' + pdffile)
    os.system('mkdir ' + images_folder + ' 2>nul >nul')
    os.system('move ' + pdffile[0] + '*.png  ' + images_folder + ' 2>nul >nul')
    os.system('move ' + pdffile[0] + '*.jpg  ' + images_folder + ' 2>nul >nul')
    os.system('move ' + pdffile[0] + '*.jpeg  ' + images_folder + ' 2>nul >nul')
    os.system('move ' + pdffile[0] + '*.gif  ' + images_folder + ' 2>nul >nul')
    os.system('del ' + pdffile[0] + '*.html  2>nul >nul')

# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Extract text from images using TESSERACT OCR
count_mathwords_temp = 0
try:
    if extract:
        with io.open(strings_figures,'w', encoding='utf8') as wfile:
            wfile.write('\n')

        for root, folder, files in os.walk('./'+images_folder):
            images = deepcopy(files)
            images = [i for i in images if any(extension in i for extension in ['.png','.jpg'])]

            countfigures = len(images)
            if countfigures > 1000:
                countfigures = countfigures_pdfminer
                with io.open(strings_figures,'a', encoding='utf8') as wfile:
                    wfile.write('#------------------------------------\n')
                    wfile.write('# Numero de imagens extraidas excede 1000 e o texto nao sera pos-processado. \n Verifique o documento PDF!!! \n\n')
                    wfile.write('# Number of images exceeds 1000 and the text will not be post-processed. \n Check the PDF document!!! \n\n')
                    
                    countwords = 9999
                    countnonwords = 9999
                    break

            for j in range(len(images)):
                words = ocr_core('./'+images_folder +'/'+images[j])            

                # remove breaklines
                words = words.replace('\n',' ')
                # split line in words
                words = words.split(' ')            

                # remove empty items
                while '' in words:
                    words.remove('') 
                
                words, countwords, non_words, countnonwords, count_mathwords_temp = return_categorized_words(words,countwords,countnonwords,count_mathwords_temp)

                with io.open(strings_figures,'a', encoding='utf8') as wfile:
                    wfile.write('#------------------------------------\n')
                    wfile.write('# Arquivo: \n')
                    wfile.write('{} '.format(images[j]))
                    wfile.write('\n')
                    for k in range(len(words)):
                        wfile.write('{} '.format(words[k]))
                        wfile.write('\n')
            break
except:
    countwords = 9999
    countnonwords = 9999

# ---------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Write output files

if wordsfile:
    with io.open(wordsfile,'w', encoding='utf8') as wfile:
        if countwords_text == 0:
            wfile.write('Nao foi possivel extrair e contar palavras do relatorio. \n Verifique o Documento PDF!!! \n\n')
            wfile.write('It was not possible to extract and count words from report. \n Check the PDF document!!! \n\n')
            countwords_text = 9999

        for i in range(len(counttext)):
            for j in range(len(counttext[i])):
                for k in range(len(counttext[i][j])):
                    wfile.write('{} '.format(counttext[i][j][k]))
                wfile.write('\n')

if nonwordsfile:
    with io.open(nonwordsfile,'w', encoding='utf8') as wfile:
        for i in range(len(notcounttext)):
            for j in range(len(notcounttext[i])):
                for k in range(len(notcounttext[i][j])):
                    wfile.write('{} '.format(notcounttext[i][j][k]))
                wfile.write('\n')

with io.open(logfile,'w') as wfile:
    wfile.write('Words:         {} \n'.format(countwords_text))
    wfile.write('Non-Words:     {} \n'.format(countnonwords_text)) 
    wfile.write('Figures Files: {} \n'.format(countfigures))
    wfile.write('Words in Figures: {} \n'.format(countwords))
    wfile.write('Non-Words in Figures: {} \n'.format(countnonwords))
    wfile.write('Total Num. of Pages: {} \n'.format(number_of_pages))
    wfile.write('Num. of Special Pages: {} \n'.format(count_specialpages))
    wfile.write('Words in Math Mode (Microsoft Word): {} \n'.format(count_mathwords))    
	
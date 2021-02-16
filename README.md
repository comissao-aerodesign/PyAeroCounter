# PyAeroCounter
Contador de palavras para a Competição AeroDesign // Word counter for the Aerodesign Competition

Author:  Member of [Comissao Tecnica Aerodesign](www.aeroct.com.br)

            Geovana Neves (geovanan90@gmail.com)

## 1) WINDOWS: standalone application 

Get the standalone application in the folder 'dist'

```bash
./dist/PyAeroCounter.exe
```

If you have any problem downloading the executable file, download the .zip that contains the PyAeroCounter.exe

```bash
./dist/PyAeroCounter.zip
```

This standalone application only requires MikTeK in order to execute properly, see item 3 of this file.

## 2) PyAeroCounter.exe default inputs and outputs

PyAeroCounter.exe default input is to read a PDF document named 'pdffile.pdf'.

The default outputs include a log file containing the final result as well as text files with the extract text.

PyAeroCounter.exe also extract images from the PDF document and save them into 'PDFFILE' folder. 

For different options, use the command line:

Example 1:
```bash
PyAeroCounter.exe -i EXAMPLE.pdf -d EXAMPLE_IMAGES
```

```bash
Available options:
-o : logfile filename           (string)
-w : wordsfile filename         (string)
-n : nonwordsfile filename      (string)
-d : images_folder name         (string)
-i : pdffile filename           (string)
-e : extract images             (boolean, integer: 0 or 1)
-f : strings_figures filename   (string)
-g : mathmodewords filename     (string)
```

## 3)  Dependencies - MikTeX

In order to properly handle images and its content, the user must have the following softwares installed:

### Extract images from PDF using pdftohtml - MikTeX Download:

https://miktex.org/download

### Google's Tesseract-OCR Engine

https://github.com/tesseract-ocr/tesseract   
For windows - precompiled binaries: https://digi.bib.uni-mannheim.de/tesseract/

If the user does not install the above software, PyAeroCounter.exe will not extract image and read the text from it.

## 4) For advanced users ... 
### ... that want to run the source code, it is necessary to install python and the following packages:

pdfminer3

pytesseract   (It requires the installation of the Google's Tesseract-OCR Engine)

------ Check the source code for more information.



WARNING: 
The pdfminer3 package was modified during the development of the PyAeroCounter script.

Substitute the following installed scripts in your computer for the ones provided in 'auxiliar' folder:

```bash
   cmapdb.py
   converter.py
```
   
   
   
### ... that want to compile the source code, use pyinstaller.

Get it: https://pypi.org/project/pyinstaller/

```bash
pyinstaller --onefile --nowindowed PyAeroCounter.py
```

## 5) Contact 

If you have any problem or suggestion, please send it to www.aeroct.com.br

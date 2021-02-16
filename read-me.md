# PyAeroCounter
 
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

Available options:
-o : logfile filename           (string)
-w : wordsfile filename         (string)
-n : nonwordsfile filename      (string)
-d : images_folder name         (string)
-i : pdffile filename           (string)
-e : extract images             (boolean, integer: 0 or 1)
-f : strings_figures filename   (string)
-g : mathmodewords filename     (string)

## 3)  Dependencies - MikTeX

The user must have the following software installed:
Extract images from PDF using pdftohtml (miktex)

Download:
https://miktex.org/download
https://miktex.org/packages/miktex-poppler-bin-2.9/files
Installed file path example: C:\Program Files\MiKTeX 2.9\miktex\bin\x64\pdftohtml.exe
	  
	  
## 4) For advanced users ... 
### that want to run the source code, it is necessary to install python and the following packages:

pdfminer3
pyteressact   (It requires the installation of the Google's Tesseract-OCR Engine)

------ Check the source code for more information.

WARNING: 
The pdfminer3 package was modified during the development of the PyAeroCounter script.
Substitute the following installed scripts in your computer for the ones provided in 'auxiliar' folder:

   cmapdb.py
   converter.py
   
### that want to compile the source code, use pyinstaller.

Get it: https://pypi.org/project/pyinstaller/

```bash
pyinstaller --onefile --nowindowed PyAeroCounter.py
```

## 5) Contact 

If you have any problem or suggestion, please send it to www.aeroct.com.br
import json
import wget
import subprocess
from pprint import pprint




#Read the json file obtained from the crawler script.  
with open('intro/lavanguardia.json') as f:
    data = json.load(f)

#pprint(data)


#subprocess.call(['/bin/ls', 'intro'])
#subprocess.call("/usr/bin/ch_pdf_png.sh")
#subprocess.call("/usr/bin/ch_pdf_png.sh")

#Recorrer el json iterativamente y descargar los pdf en el directorio downloadPDF

for song in data:
	for key, value in song.items():
		if key=='PDF_URL':
			print(value)
			list = value
			for subtring in list:
				filename = wget.download(subtring, out="downloadPDF")
				print(subtring)

#Transformar pdfs a png 
subprocess.call("/usr/bin/ch_pdf_png.sh")

#Eliminar los pdfs descargados.
subprocess.call("/usr/bin/del_pdfs.sh")

#list = data[0]['PDF_URL']

#for subtring in list:
#	print(subtring)


#subtring = subtring.replace("[","]","")
#print("Este dato es:", subtring)


#Download PDF
#filename = wget.download(subtring, out="downloadPDF")

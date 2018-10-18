import json
import wget
import subprocess
from pprint import pprint



#Read the json file obtained from the crawler script.  
with open('intro/lavanguardia.json') as f:
    data = json.load(f)


#Go through the jason file iteratively and download the pdfs in the downloadPDF directory
for song in data:
	for key, value in song.items():
		if key=='PDF_URL':
			print(value)
			list = value
			for subtring in list:
				filename = wget.download(subtring, out="downloadPDF")
				print(subtring)

#Transform the pdf to png using the package ImageMagic with the convert option. Also the
#module subprocess is used to execute the script in bash. 
subprocess.call("/usr/bin/ch_pdf_png.sh")

#Delete files pdfs inside  downloadPDF  directory after of conversion done.  
subprocess.call("/usr/bin/del_pdfs.sh")
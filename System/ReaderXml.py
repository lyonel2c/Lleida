## Funcion que realiza la segmentacion de una imagen ej fuente.png en funcion de la desc
## descripcion del archivo fuente.png.xml.
## Hay que diseñar la funcion que realice esto de manera distribuida.

from os import listdir
from os.path import isfile, join
import os
import json 
import shutil
import glob
import ast
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from lxml import etree
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter




def convert_png_txt(file_png):
	im = Image.open(file_png)
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('1')
	file_png = file_png + ".tmp"
	im.save(file_png)
	text = pytesseract.image_to_string(Image.open(file_png))
	file_txt = file_png + ".txt"
	f = open(file_txt, "w")
	f.write(text)
	f.close()




def get_directory_relative_name(name_directory):
	print("hola")
	print(name_directory)
	position = ([pos for pos, char in enumerate(name_directory) if char == '/'])
	base_name = name_directory
	name_directory = name_directory[max(position):]
	name_directory = base_name + name_directory
	print("Final file:"+name_directory)
	return name_directory


def get_name_png(name_directory):
	position = ([pos for pos, char in enumerate(name_directory) if char == '/'])
	base_name = name_directory
	name_directory = name_directory[max(position):]
	name_directory = name_directory.replace(".xml","")
	name_directory = base_name + name_directory
	print("Esto es el archivo png a tratar:" + name_directory)
	return name_directory



def segmentation_file(regions, file_name, num_region):
	print("Este es mi filename:"+file_name)
	#image = cv2.imread(file_name, -1)
	position = ([pos for pos, char in enumerate(file_name) if char == '/'])
	base_name = file_name[:max(position)]
	complement_name = file_name[max(position):]
	image = cv2.imread(file_name)
	complement_name = complement_name.replace('.png','')
	complement_name = complement_name+str(num_region)+".png"
	file_name_seg = base_name+complement_name 
	print(file_name_seg)
	mask = np.zeros(image.shape, dtype=np.uint8)
	roi_corners_list = ast.literal_eval(regions)
	roi_corners = np.array(roi_corners_list, dtype=np.int32)
	for arrays in roi_corners:
		print(arrays)
	channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
	ignore_mask_color = (255,)*channel_count
	cv2.fillPoly(mask, roi_corners, ignore_mask_color)
	masked_image = cv2.bitwise_and(image, mask)
	cv2.imwrite(file_name_seg, masked_image)
	#Transform jpg to txt
	convert_png_txt(file_name_seg)

	# from Masterfool: use cv2.fillConvexPoly if you know it's convex


def read_xml_segmentation_file(file_name_xml, file_name):

#	doc = etree.parse('lore-1.png.xml')
	#print(file_name_xml)
	doc = etree.parse(file_name_xml)
	#print(file_name_xml)
	raiz = doc.getroot()
	page = raiz[1]
	item_region = 0
	for regions in page:
		region = "[["
		for coords in regions:
			for h in coords:
				region = region+"("+h.attrib["x"]+","+h.attrib["y"]+"), "
			region = region[:-2]
			region = region+"]]"
			print(item_region)
			print(region)
		#	segmentation_file(region,"lore-1.png",item_region)
			segmentation_file(region,file_name,item_region)
		item_region = item_region+1
	print("lectura realizada."+str(item_region))


def set_segment_png_files(mi_path):
	#solo_directorios = [os.path.abspath(name) for name in os.listdir(mi_path)]
	solo_directorios = os.listdir(mi_path)
	for nombres in solo_directorios:
		print(mi_path+nombres)
		#print(get_directory_relative_name(nombres)) 
		#print(get_name_png(nombres))
		read_xml_segmentation_file(get_directory_relative_name(mi_path+nombres),get_name_png(mi_path+nombres))
		

############################################################################

# Load the name of directory which has the files that will be read and subdivided into images. 
config_file = json.loads(open('cfg/conf.json').read())
segmentation_source = config_file['segmentation_source']

set_segment_png_files(segmentation_source)
#read_xml_segmentation_file('/home/lyonel/Dropbox/LLEIDA/BBVA/system/downloadPDF/segment/VAS19970910-013.pdf.png.xml/VAS19970910-013.pdf.png.xml','/home/lyonel/Dropbox/LLEIDA/BBVA/system/downloadPDF/segment/VAS19970910-013.pdf.png.xml/VAS19970910-013.pdf.png')

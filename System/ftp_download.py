from ftplib import FTP
import os
import json


###Read configuration file


config_file = json.loads(open('cfg/conf.json').read())
print("configuracion exitosa")

local_directory = config_file['local_root_directory']
directory = config_file['remote_root_directory']
ip = config_file['ftp_server']
password = config_file['password']
user = config_file['user']
port = 21

print (ip)

ftp = FTP(ip)
ftp.login(user,password)
print("Lista de archivos:") 

filematch = '*.*'


def connect_ftp_Server(ip,user,passwd, local_directory, remote_directory):
	ftp = FTP(ip)
	fpt.login(user,passwd)
	os.chdir(local_directory)
	ftp.cwd(remote_directory)


def download_files(directory, filematch, local_directory, ip, user, passwd):
	os.chdir(local_directory)
	ftp.cwd(directory)
	files = ftp.dir()

	for filename in ftp.nlst(filematch): # Loop - looking for matching files
	    fhandle = open(filename, 'wb')
	    print('Getting ' + filename) #for confort sake, shows the file that's being retrieved
	    ftp.retrbinary('RETR ' + filename, fhandle.write)
	    fhandle.close()

def ftp_upload(localfile, remotefile):
	fp = open(localfile, 'rb')
	ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
	fp.close()
	print("after upload " + localfile + " to " + remotefile)


def upload_img(file, local_directory):
	ftp_upload(local_directory + "/" + file, file)


def upload_files(directory, local_directory):

	os.chdir(local_directory)
	ftp.cwd(directory)
	currentlist = os.listdir(local_directory)
	newfiles = list(set(currentlist))
	for needupload in newfiles:
		upload_img(needupload, local_directory)

download_files(directory, filematch, local_directory,ip,user,password)
#upload_files(directory, local_directory)

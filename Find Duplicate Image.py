import os
import shutil
# import mysql.connector
from PIL import Image, ImageStat
from fnmatch import fnmatch
import time
import hashlib
# import imagehash
from tkinter import Tk, filedialog
import numpy as np
#query out the database for known user_id
def Query():
	mydb = mysql.connector.connect(
	  host="10.235.94.91",
	  user=input("Username: "),
	  password=input("Password: "),
	  database="MACARONS"
	)
	mycursor = mydb.cursor()

	mycursor.execute("SELECT * FROM R177_2021_AP1_Step16_Processing")

	myresult = mycursor.fetchall()

#Create Directory put Output
def	CreateFolderOut(imagePath):
	opFolName = 'Image_Duplicate'
	nFolPath = os.path.join(imgoutpath, opFolName)
	directory = os.path.dirname(nFolPath)
	if not os.path.exists(directory):
		os.makedirs(nFolPath)
	else:
		shutil.rmtree(nFolPath, ignore_errors=True)
		os.makedirs(nFolPath)
	return nFolPath

def deletefolpath(path):
    shutil.rmtree(path, ignore_errors=True)

def hash(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        chuck = f.read(8192)
        while chuck:
            file_hash.update(chuck)
            chuck = f.read(8192)
    return (file_hash.hexdigest())

def averagehash(file):
    with Image.open(file) as img:
        temp_hash = imagehash.average_hash(img, 9)
    return temp_hash


def getfilearray(path):
    arraypath = []
    for file in os.listdir(path):
        arraypath.append(file)
    return arraypath

root = Tk()
root.withdraw()
root.attributes('-topmost', True)
firstpath = filedialog.askdirectory()
foundimg = []
imgoutpath = firstpath
opFolName = 'Image_Duplicate'
nFolPath = os.path.join(imgoutpath, opFolName)

def main():
    c = 0
    d = 0
    nFolPath = CreateFolderOut(imgoutpath)
    deletefolpath(nFolPath)
    hashdict = {}
    arraypath = getfilearray(firstpath)
    print('Calculating Images Hash')
    for i in arraypath:
        imagepath = os.path.join(firstpath,i)
        hashdict[i] = hash(imagepath)
    print('Image Hashing Done!!!')
    print('Comparing All the hashes')
    for i in arraypath:
        finalpath = os.path.join(firstpath,i)
        print ('Current Looking Image:', i)
        if finalpath in foundimg:
            print ("Found Previous Image:", i)
            continue
    #
    #     # image_org = Image.open(finalpath)
    #     # pix_mean1 = ImageStat.Stat(image_org).mean
        pix_mean1 = hashdict[i]
        for j in arraypath:
            j = os.path.join(firstpath, j)
            j1 = os.path.relpath(j, firstpath)
            if j != finalpath:
    #            # image_org2 = Image.open(j)
    #             # pix_mean2 = ImageStat.Stat(image_org2).mean
                pix_mean2 = hashdict[j1]
                if pix_mean1 == pix_mean2:
                    foundimg.append(j)
                    print ('Found Duplicated Image:',len(foundimg))
                    print ('File:', finalpath,'and', j)
                    if c == 0:
                        nFolPath = CreateFolderOut(imgoutpath)
                        c = c + 1
                    shutil.copy(finalpath, nFolPath)
                    shutil.copy(j, nFolPath)
    print ('Total Images Lookup:', len(arraypath))
    print ('Found Duplicated Image:', len(foundimg))
    print ('Program Completed')

        # for file in os.listdir(finalpath):
        #     folName = os.fsdecode(file)
        #     print (folName)
        #     if folName == opFolName:
        #         continue
        #     if not fnmatch(folName, pattern):
        #         imagePath = os.path.join(firstpath, folName)
        #         imageFiles = [f for f in os.listdir(finalpath) if f[-4:].lower() == ".png" or f[-4:].lower() == ".jpg" or f[-4:].lower == 'jpeg']
        #         #print(imageFiles)
        #         duplicate_files = []
        #         for file_org in imageFiles:
        #             if not file_org in duplicate_files:
        #                 imOrgPath = os.path.join(imagePath, file_org)
        #                 image_org = Image.open(imOrgPath)
        #                 pix_mean1 = ImageStat.Stat(image_org).mean
        #
        #                 for file_check in imageFiles:
        #                     if file_check != file_org:
        #                         imCheckPath = os.path.join(imagePath, file_check)
        #                         image_check = Image.open(imCheckPath)
        #                         pix_mean2 = ImageStat.Stat(image_check).mean
        #
        #                         if pix_mean1 == pix_mean2:
        #                             if c == 0:
        #                                 nFolPath = CreateFolderOut(firstpath)
        #                                 c = c + 1
        #                             #print(nFolPath)
        #                             shutil.copy(imOrgPath, nFolPath)
        #                             shutil.copy(imCheckPath, nFolPath)
        #                             duplicate_files.append((file_org))
        #                             duplicate_files.append((file_check))
        #
        #         print(list(dict.fromkeys(duplicate_files)))
        #         print ("Completed.!!!!!")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Elapsed Time: "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
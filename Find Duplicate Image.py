import os
import shutil
import mysql.connector
from PIL import Image, ImageStat
from fnmatch import fnmatch
import copy
import time

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

def ResultExist():
	return os.path.exists(nFolPath)

firstpath = r"C:\Users\patchnui\Downloads\Python_Test\Upload"
imgoutpath = r"C:\Users\patchnui\Downloads\Python_Test\\"
pattern = "*.py"
opFolName = 'Image_Duplicate'
nFolPath = os.path.join(imgoutpath, opFolName)
arraypath = copy.main(firstpath)
foundimg = []

def main():
    c = 0
    for i in arraypath:
        finalpath = str(i)
        print ('Current Looking Image:', i)
        if i in foundimg:
            print ("Found Previous Image:", i)
            continue
        image_org = Image.open(finalpath)
        pix_mean1 = ImageStat.Stat(image_org).mean
        for j in arraypath:
            j = str(j)
            if j != i:
                image_org2 = Image.open(j)
                pix_mean2 = ImageStat.Stat(image_org2).mean
                if pix_mean1 == pix_mean2:
                    foundimg.append(j)
                    print ('Found Duplicated Image:',len(foundimg))
                    print ('File:', finalpath, j)
                    if c == 0:
                        nFolPath = CreateFolderOut(imgoutpath)
                        c = c + 1
                    shutil.copy(finalpath, nFolPath)
                    shutil.copy(j, nFolPath)
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
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
import os
import shutil
import mysql.connector
from PIL import Image, ImageStat
from fnmatch import fnmatch

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
	nFolPath = os.path.join(firstpath, opFolName)
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
pattern = "*.py"
opFolName = 'Image_Duplicate'
nFolPath = os.path.join(firstpath, opFolName)
c = 0
month = 12,12
day = 1,2


def main():
	for i in month:
		i = str(i)
		newpath = os.path.join(firstpath, i)
		for j in day:
			j = str(j)
			finalpath = os.path.join(newpath, j)

			for file in os.listdir(finalpath):
				folName = os.fsdecode(file)
				print (folName)
				if folName == opFolName:
					continue
				if not fnmatch(folName, pattern):
					imagePath = os.path.join(firstpath, folName)
					imageFiles = [f for f in os.listdir(finalpath) if f[-4:].lower() == ".png" or f[-4:].lower() == ".jpg" or f[-4:].lower == 'jpeg']
					#print(imageFiles)
					duplicate_files = []
					for file_org in imageFiles:
						if not file_org in duplicate_files:
							imOrgPath = os.path.join(imagePath, file_org)
							image_org = Image.open(imOrgPath)
							pix_mean1 = ImageStat.Stat(image_org).mean

							for file_check in imageFiles:
								if file_check != file_org:
									imCheckPath = os.path.join(imagePath, file_check)
									image_check = Image.open(imCheckPath)
									pix_mean2 = ImageStat.Stat(image_check).mean

									if pix_mean1 == pix_mean2:
										if c == 0:
											nFolPath = CreateFolderOut(firstpath)
											c = c + 1
										#print(nFolPath)
										shutil.copy(imOrgPath, nFolPath)
										shutil.copy(imCheckPath, nFolPath)
										duplicate_files.append((file_org))
										duplicate_files.append((file_check))

					print(list(dict.fromkeys(duplicate_files)))
					print ("Completed.!!!!!")

if __name__ == "__main__":
	main()
import os
from PIL import Image, ImageStat
import shutil

#Create Directory put Output
def CreateFolderOut(imagePath):
    opFolName = 'Image_Duplicate'
    nFolPath = os.path.join(imagePath, opFolName)
    directory = os.path.dirname(nFolPath)

    if not os.path.exists(directory):
      os.makedirs(nFolPath)
    else:
      shutil.rmtree(nFolPath, ignore_errors=True)
      os.makedirs(nFolPath)
    return nFolPath


imagePath = r'C:\Users\wasinthu\Downloads\Python_Test\Image_Test_Python'
imageFiles = [f for f in os.listdir(imagePath) if f[-4:].lower() == '.png']
print(imageFiles)

folderPath = os.path.dirname(imagePath)
#print(folderPath)
folderName = os.path.basename(imagePath)
#print(folderName)

#Rename File Image Name
for file in imageFiles:
   oldName = imagePath + '/' + file
   #print(oldName)
   
   newName = imagePath + '/' + folderName + "_" + file
   #print(newName)
   os.rename(oldName, newName)

#Replace File Image Name
# for file in imageFiles:
#    nameReplace =  file.replace(folderName + "_", '')
#    if nameReplace != file:
#        oldName2 = imagePath + '/' + file
#        print(oldName2)

#        newName2 = imagePath + '/' + nameReplace
#        print(newName2)
#        os.rename(oldName2, newName2)

print('#####################################################################')
duplicate_files = []

imageFiles = [f for f in os.listdir(imagePath) if f[-4:].lower() == '.png']
c = 0
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
                    nFolPath = CreateFolderOut(imagePath)
                    c = c + 1
                    #print(nFolPath)
                  shutil.copy(imOrgPath, nFolPath)
                  # newName = imagePath + '/' + folderName + "_" + file
                  # os.rename(oldName, newName)
                  shutil.copy(imCheckPath, nFolPath)
                  duplicate_files.append((file_org))
                  duplicate_files.append((file_check))

print(list(dict.fromkeys(duplicate_files)))
print ("Completed.!!!!!")






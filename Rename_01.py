import os
from PIL import Image, ImageStat

#Create Directory put Output
def CreateFolderOut(imagePath):

    directory = 'Image_Duplicate'
    path = os.path.join(imagePath, directory)
    os.mkdir(path)

    print("Directory '% s' created" % directory)


imagePath = r'C:\Users\wasinthu\Downloads\Python_Test\Image_Test_Python'
imageFiles = [f for f in os.listdir(imagePath) if f[-4:].lower() == '.png']
print(imageFiles)

folderPath = os.path.dirname(imagePath)
#print(folderPath)
folderName = os.path.basename(imagePath)
#print(folderName)

#Rename File Image Name
##for file in imageFiles:
##    oldName = imagePath + '/' + file
##    print(oldName)
##    
##    newName = imagePath + '/' + folderName + "_" + file
##    print(newName)
##    
##    os.rename(oldName, newName)

#Replace File Image Name
##for file in imageFiles:
##    nameReplace =  file.replace(folderName + "_", '')
##    if nameReplace != file:
##        oldName2 = imagePath + '/' + file
##        print(oldName2)
##
##        newName2 = imagePath + '/' + nameReplace
##        print(newName2)
##        os.rename(oldName2, newName2)

print('#####################################################################')
duplicate_files = []

for file_org in imageFiles:
    if not file_org in duplicate_files:
        image_org = Image.open(os.path.join(imagePath, file_org))
        pix_mean1 = ImageStat.Stat(image_org).mean

        for file_check in imageFiles:
            if file_check != file_org:
                image_check = Image.open(os.path.join(imagePath, file_check))
                pix_mean2 = ImageStat.Stat(image_check).mean

                if pix_mean1 == pix_mean2:
                    duplicate_files.append((file_org))
                    duplicate_files.append((file_check))

##CreateFolderOut(imagePath)
##print(list(dict.fromkeys(duplicate_files)))
a = list(dict.fromkeys(duplicate_files))

##for i in duplicate_files:

    print(*duplicate_files)





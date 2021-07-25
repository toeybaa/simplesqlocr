# -*- coding: utf-8 -*-
import csv
import os
# import pandas as pd
import os
from tkinter import Tk, filedialog
import shutil


user = []
imgfolder = []
finaldir = []
root = Tk()
root.withdraw()
root.attributes('-topmost', True)
print ('Image Directory:',os.getcwd())
# imgoutpath = r"C:\\Users\\patchnui\\Downloads\\Python_Test\\"
imgoutpath = filedialog.askdirectory(title='Choose Image Destination Folder')
opFolName = 'Image_Duplicate'
nFolPath = os.path.join(imgoutpath, opFolName)
print ('Result Directory:',nFolPath)

def readcsvfile():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file = filedialog.askopenfilename(title='CSV file for selecting user')
    print ('Looking CSV file:',file)
    with open(file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            user.append(row[1])

def listdirs(rootdir):
    # for root, dirs, files in os.walk(rootdir):
    #     if not dirs:
    #         imgfolder.append(root)
    return (rootdir)

def getabspath(path):
    img = []
    dir = []
    readcsvfile()
    imgfolder = listdirs(path)
    for file in os.listdir(imgfolder):
        if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
            img.append(os.path.join(imgfolder,file))
    for i in img:
        for j in user:
            if j in i:
                dir.append(i)
    return (dir)
    # for i in imgfolder:
    #     i = str(i)+'\\'
    #     for file in os.listdir(i):
    #
    #     for i in img:
    #         for j in user:
    #             if j in i:
    #                 dir.append(i)
    #     dir = list(dict.fromkeys(dir))
    #
    # return (dir)

def main():
    dir = getabspath(os.getcwd())
    dest = imgoutpath
    c = 0
    for i in dir:
        print ('Copying:', i, 'to', dest)
        shutil.copy(i, dest)
        c += 1
    print ('Successfully copied', c, 'images to', dest)
    input("Press Any Key to close the program")
    return dest

if __name__ == "__main__":
    main()
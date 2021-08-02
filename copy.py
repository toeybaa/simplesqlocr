# -*- coding: utf-8 -*-
import csv
import os
# import pandas as pd
import os
from tkinter import Tk, filedialog
import shutil


imgfolder = []
finaldir = []


def readcsvfile():
    user = []
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file = filedialog.askopenfilename(title='CSV file for selecting user')
    print ('Looking CSV file:',file)
    with open(file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            user.append(row[1])
    return (user)

def remove_duplicates(l):
    return list(set(l))

def listdirs(rootdir):
    dirlist = []
    for root, dirs, files in os.walk(rootdir):
        if not dirs:
            dirlist.append(root)
    return (dirlist)


def getabspath(path):
    img = []
    dir = []
    user = readcsvfile()
    imgfolder = listdirs(path)
    user = set(user)
    for a in imgfolder:
        for file in os.listdir(a):
            if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
                print (a, file)
                img.append(os.path.join(a,file))
        for i in user:
            for j in img:
                if i in j:
                    # print (i, j)
                    dir.append(j)
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
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder = filedialog.askdirectory(title='Choose Source Folder')
    folderout = filedialog.askdirectory(title='Choose Image Destination Folder')
    dir = getabspath(folder)
    dest = folderout
    for i in dir:
        print ('Copying:', i, 'to', dest)
        shutil.copy(i, dest)
    print ('Successfully copied', len(dir), 'images to', dest)
    input("Press Any Key to close the program")
    return dest

if __name__ == "__main__":
    main()
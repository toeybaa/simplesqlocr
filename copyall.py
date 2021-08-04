# -*- coding: utf-8 -*-
import csv
import os
# import pandas as pd
import os
from tkinter import Tk, filedialog
import shutil
import imagehash
from PIL import Image
from itertools import chain

imgfolder = []
finaldir = []
hashdict = {}

def averagehash(file):
    with Image.open(file) as img:
        temp_hash = imagehash.average_hash(img, 9)
    return temp_hash

def getfilearray(path):
    arraypath = []
    for file in os.listdir(path):
        arraypath.append(file)
    return arraypath

def readcsvfile():
    user = []
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file = filedialog.askopenfilename(title='CSV file for selecting user')
    print ('Chosen CSV file:',file)
    with open(file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            user.append(row[1])
    return (user)

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

def listdirs(rootdir):
    # dirlist = []
    # for root, dirs, files in os.walk(rootdir):
    #     if not dirs:
    #         dirlist.append(root)
    return (rootdir)

def getabspath(path, path2):
    img = []
    dir = 0
    d = 0
    opFolName = 'Image_Duplicate'
    user = readcsvfile()
    # imgfolder = getallpath(path)
    imgfolder = [r'D:\Upload\12\1', r'D:\Upload\12\2']
    user = set(user)
    print('Calculating Images Hash...')
    for a in imgfolder:
        c = 0
        print ('Looking Images Folder', a, end=' >>> ')
        if a == r'W:\Upload\2019\1\1':
            break
        for file in os.listdir(a):
            if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
                for i in user:
                    if i in file:
                        path1 = os.path.join(a,file)
                        hashdict[path1] = (averagehash(path1))
                        # print (path1, averagehash(path1))
                        c += 1
        if c != 0:
            print (c, 'suspect images hashed')
        if c == 0:
            print ('No suspect images found')
    print ('Total Image hashed:', len(hashdict))
    dupimglist = dupdict(hashdict)
    print ('Total Number of similar hashes:', len(dupimglist))
    for i in dupimglist:
        temp = str(hashdict.get(list(i)[0]))
        nFolPath = os.path.join(path2, opFolName)
        hashfolder = os.path.join(nFolPath, temp)
        for k in i:
            # print (temp, k)
            if not os.path.exists(hashfolder):
                os.makedirs(hashfolder)
            copy(k, hashfolder)
            d += 1
    print('Total Number of similar images:', d)

    print('Image Hashing Done!!!')
    print('Comparing All the hashes')
    # #     for i in user:
    # #         for j in img:
    # #             if i in j:
    # #                 # print (i, j)
    # #                 dir.append(j)
    # #                 # print ('Getting:', j)
    # # print (len(dir))
    # return (dir)

def dupdict(dictA):
    dictB = {}
    for key, value in dictA.items():
        dictB.setdefault(value, set()).add(key)
    res = filter(lambda x: len(x) > 1, dictB.values())
    return (list(res))

def copy(path1 ,path2):
    shutil.copy(path1, path2)
    print ('Copying:', path1, 'to', path2)

def getallpath(path):
    year = [2018, 2019]
    fpath = []
    for i in year:
        i = str(i)
        if i == '2018':
            month = list(range(6, 13))
            for j in month:
                j = str(j)
                if j == '6' or j == '9' or j == '11':
                    day = list(range(1, 31))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '7' or j == '8' or j == '10' or j == '12':
                    day = list(range(1, 32))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
        if i == '2019':
            month = list(range(1, 13))
            for j in month:
                j = str(j)
                if j == '4' or j == '6' or j == '9' or j == '11':
                    day = list(range(1, 31))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '1' or j =='3' or j == '5' or j == '7' or j == '8' or j == '10' or j == '12':
                    day = list(range(1, 32))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '2':
                    day = list(range(1, 29))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))

    return (fpath)

def main():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder = filedialog.askdirectory(title='Choose Source Folder')
    folderout = filedialog.askdirectory(title='Choose Image Destination Folder')
    folder = 'W:\\Upload'
    dir = getabspath(folder, folderout)
    dest = folderout
    # for i in dir:
    #     print ('Copying:', i, 'to', dest)
    #     shutil.copy(i, dest)
    print ('Successfully copied', dir, 'images to', dest)
    return dest

if __name__ == "__main__":
    main()

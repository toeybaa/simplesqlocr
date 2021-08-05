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
import time
import hashlib

imgfolder = []
finaldir = []
hashdict = {}

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
    imgfolder = getallpath(path, (int)(input("choose year: ")))
    print ('i', imgfolder)
    # imgfolder = [r'W:\upload\2018\12\1', r'W:\upload\2018\12\2', r'W:\upload\2018\12\3', r'W:\upload\2018\12\4']
    user = set(user)
    print('Calculating Images Hash...')
    start = time.time()
    for a in imgfolder:
        c = 0
        print ('Looking Images Folder', a, end=' >>> ')
        if a == r'W:\Upload\2019\1\1':
            break
        for file in os.listdir(a):
            # print ('Current file hasing:',file)
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
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print('Image Hashing Done!!!')
    print ('Total Image hashed:', len(hashdict))
    print ("Hashing Took: "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds),
           '>>>','Per image:',str("{:.2f}".format(((end-start)/len(hashdict))*1000)), 'ms')
    dupimglist = dupdict(hashdict)
    print('Comparing All the hashes...')
    print ('Total Number of similar hashes:', len(dupimglist))
    print ('Start copying all images with similar hash...')
    startcopy = time.time()
    for i in dupimglist:
        temp = str(hashdict.get(list(i)[0]))
        nFolPath = os.path.join(path2, opFolName)
        hashfolder = os.path.join(nFolPath, temp)
        for k in i:
            if not os.path.exists(hashfolder):
                os.makedirs(hashfolder)
            copy(k, hashfolder)
            d += 1
    endcopy = time.time()
    hourscopy, remcopy = divmod(end - start, 3600)
    minutescopy, secondscopy = divmod(rem, 60)
    print('Total Number of similar images:', d)
    print('Successfully copied', d, 'images to', nFolPath)
    print("Copying Took: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hourscopy), int(minutescopy), secondscopy),
          '>>>', 'Per image:', str("{:.2f}".format(((endcopy - startcopy) / d) * 1000)), 'ms')


def dupdict(dictA):
    dictB = {}
    for key, value in dictA.items():
        dictB.setdefault(value, set()).add(key)
    res = filter(lambda x: len(x) > 1, dictB.values())
    return (list(res))

def copy(path1 ,path2):
    shutil.copy(path1, path2)
    print ('Copying:', path1, 'to', path2)

def getallpath(path, years):
    year = [2018, 2019]
    fpath = []
    for i in year:
        i = str(i)
        if (str)(years)==(str)(i) and years == 2018:
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
        if (str)(years)==(str)(i) and years == 2019:
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
    # folder = filedialog.askdirectory(title='Choose Source Folder')
    # folderout = filedialog.askdirectory(title='Choose Image Destination Folder')
    folderout = r'D:\ImgOut'
    folder = 'D:\\Upload'
    dir = getabspath(folder, folderout)
    dest = folderout
    # for i in dir:
    #     print ('Copying:', i, 'to', dest)
    #     shutil.copy(i, dest)
    print ('Program Completed!!!')
    return dest

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Elapsed Time: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
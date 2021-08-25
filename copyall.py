# -*- coding: utf-8 -*-
import csv
import os
# import pandas as pd
import os
from tkinter import Tk, filedialog
import shutil
import logging

import PIL
import imagehash
from PIL import Image, ImageStat
from itertools import chain
import time
import hashlib
import numpy as np
import datetime
import sys
from collections import Counter

imgfolder = []
finaldir = []
hashdict = {}
problemfiles = []
d = 0
customer_count = 0


def hash(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        chuck = f.read(8192)
        while chuck:
            file_hash.update(chuck)
            chuck = f.read(8192)
    return (file_hash.hexdigest())


def averagehash(file):
    try:
        with Image.open(file) as img:
            temp_hash = imagehash.dhash(img, 10)
            # print (temp_hash)
    except PIL.UnidentifiedImageError:
        temp_hash = 'Corrupted Files'
        problemfiles.append(file)
    except Exception as e:
        temp_hash = str(e)
    return temp_hash


def meanimg(file):
    try:
        with Image.open(file) as img:
            temp_mean = ImageStat.Stat(img).mean
            print(file, temp_mean)
    except PIL.UnidentifiedImageError:
        temp_mean = 'Corrupted Files'
    except Exception as e:
        temp_mean = str(e)
    return temp_mean


def getfilearray(path):
    arraypath = []
    for file in os.listdir(path):
        arraypath.append(file)
    return arraypath


def readcsvfile(path):
    user = []
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    title = 'CSV file for selecting user in ' + sys.argv[1]
    file = filedialog.askopenfilename(title=title)
    print('Chosen CSV file:', file)
    with open(file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            user.append(row[1])
    return (user)


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def listdirs(rootdir):
    return (rootdir)


def checkyear(year):
    now = datetime.datetime.now()
    dateyear = now.year
    return year >= 2018 and year <= dateyear


def getpathhashcopy(path, path2):
    dir = 0
    opFolName = 'Image_Duplicate'
    opFolName2 = 'Customer_Duplicate'
    user = readcsvfile(path2)
    y = int(sys.argv[1])
    flag = checkyear(y)
    while not flag:
        print('Year', y, 'was not found in image folder')
        y = int(input("Please choose year between 2018 and current year: "))
        if checkyear(y):
            break
    # imgfolder = getallpath(path, y)
    # imgfolder = [r'W:\upload\2018\12\1', r'W:\upload\2018\12\2', r'W:\upload\2018\12\3', r'W:\upload\2018\12\4']
    imgfolder = [r'D:\Users\Peth\Downloads\Python_Result\Image', r'D:\Users\Peth\Downloads\Python_Result\Image2']
    user = set(user)
    print('Calculating Images Hash...')
    start = time.time()
    for a in imgfolder:
        c = 0
        print('Looking Images Folder', a, end=' >>> ')
        try:
            for file in os.listdir(a):
                if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
                    for i in user:
                        if i in file:
                            path1 = os.path.join(a, file)
                            hashdict[path1] = averagehash(path1)
                            c += 1
        except OSError as e:
            print(e, end=' >>> ')
        if c != 0:
            print(c, 'suspect images hashed')
        if c == 0:
            print('No suspect images found')

    dupimglist = dupdict(hashdict)
    end = time.time()
    startcopy = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print('Image Hashing Done!!!')
    print('Total Image hashed:', len(hashdict))
    if len(hashdict) != 0:
        print("Hashing Took: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds),
              '>>>', 'Per image:', str("{:.2f}".format(((end - start) / len(hashdict)) * 1000)), 'ms')
    print('Comparing All the hashes...')
    print('Total Number of similar hashes:', len(dupimglist))
    print('Start copying all images with similar hash...')
    nFolPath = os.path.join(path2, opFolName)
    nFolPath2 = os.path.join(path2, opFolName2)
    for i in dupimglist:
        temp = str(hashdict.get(list(i)[0]))
        if '0000000000000000000000000' in temp or '00c0500c0500c0301c0702c05' in temp\
                or '00000000000000000000000' in temp or '0000000000000000000000002' in temp or '0000000000000000000000400' in temp\
                or 'ffffffffffffffffffffffdff' in temp or 'ffffffffffffffffffffffff' in temp or '000000000000000000000' in temp:
            continue
        customer = []
        file = []
        dir += 1
        hashfolder = os.path.join(nFolPath, temp)
        hashfolder2 = os.path.join(nFolPath2, temp)
        for k in i:
            customer.append(getcustomer(k))
            file.append(k)
        if len(odd_occurring_num(customer)) >= 2:
            for j in file:
                copy(j, hashfolder)
        if len(even_occurring_num(customer)) >= 2:
            for j in file:
                copycustomer(j, hashfolder2)
    print('Total Number of same images with different customer number:', d)
    print('Total Number of same images with same customer number:', customer_count)
    print('Successfully copied', d, 'images to', nFolPath)
    print('Successfully copied', customer_count, 'images to', nFolPath2)
    endcopy = time.time()
    hourscopy, remcopy = divmod(endcopy - startcopy, 3600)
    minutescopy, secondscopy = divmod(remcopy, 60)
    if d != 0 and flag != 0:
        print("Copying Took: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hourscopy), int(minutescopy), secondscopy),
          '>>>', 'Per image:', str("{:.2f}".format(((endcopy - startcopy) / (d+customer_count)) * 1000)), 'ms')
    if flag == 0:
        print("No Similar Image Duplicate Found!")
    if d == 0:
        print("No Exact Image Duplicate Found!")
    if d >= 0:
        return True
    else:
        return False


def dupdict(dictA):
    dictB = {}
    for key, value in dictA.items():
        dictB.setdefault(value, set()).add(key)
    res = filter(lambda x: len(x) > 1, dictB.values())
    return (list(res))


def copy(path1, path2):
    if not os.path.exists(path2):
        os.makedirs(path2)
    shutil.copy(path1, path2)
    global d
    d += 1


def copycustomer(path1, path2):
    if not os.path.exists(path2):
        os.makedirs(path2)
    shutil.copy(path1, path2)
    global customer_count
    customer_count += 1

def calculate(dict, path):
    flag = False
    c = 0
    for i in dict:
        t1 = (dict[i])
        for j in dict:
            if not i == j:
                t2 = (dict[j])
                try:
                    diff = t1 - t2
                except AttributeError as e:
                    print (e)
                if True:
                    print('c',diff)
                    flag = True
                    c += 1
                    foldername = os.path.join(path, str(dict[j]))
                    foldername = os.path.join(foldername, str(diff))
                    # copy(i, foldername)
                    # copy(j, foldername)
    return 2*c


def find_similar(dict, path):
    for i in dict:
        hash1 = dict[i].hash
        for j in dict:
            if not i == j:
                hash2 = dict[j].hash
                try:
                    print ('d', np.count_nonzero(hash1 != hash2))
                except AttributeError as e:
                    print (e)


def getcustomer(path):
    str2 = os.path.sep
    res = path.split(str2, 16)[-1]
    str3 = '_'
    res = res.split(str3, 1)[-1]
    res = res.rsplit('_')[0]
    return res


def odd_occurring_num(arr):
    return [i for i in arr if arr.count(i) < 2]


def even_occurring_num(arr):
    return [i for i in arr if arr.count(i) >= 2]

def getallpath(path, years):
    year = [2018, 2019, 2020, 2021, 2022]
    fpath = []
    for i in year:
        i = str(i)
        if (str)(years) == (str)(i) and years == 2018:
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
        if (str)(years) == (str)(i) and years == 2019:
            month = list(range(1, 13))
            for j in month:
                j = str(j)
                if j == '4' or j == '6' or j == '9' or j == '11':
                    day = list(range(1, 31))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '1' or j == '3' or j == '5' or j == '7' or j == '8' or j == '10' or j == '12':
                    day = list(range(1, 32))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '2':
                    day = list(range(1, 29))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
        if (str)(years) == (str)(i) and years == 2020:
            month = list(range(1,13))
            for j in month:
                j = str(j)
                if j == '4' or j == '6' or j == '9' or j == '11':
                    day = list(range(1, 31))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '1' or j == '3' or j == '5' or j == '7' or j == '8' or j == '10' or j == '12':
                    day = list(range(1, 32))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '2':
                    day = list(range(1, 30))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
        if (str)(years) == (str)(i) and years == 2021:
            month = list(range(1,13))
            for j in month:
                j = str(j)
                if j == '4' or j == '6' or j == '9' or j == '11':
                    day = list(range(1, 31))
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
                if j == '1' or j == '3' or j == '5' or j == '7' or j == '8' or j == '10' or j == '12':
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
    folder = r'W:\upload'
    folderout = r'D:\Python_Image_Out'
    folderout = os.path.join(folderout, str(sys.argv[1]))
    dir = getpathhashcopy(folder, folderout)
    dest = folderout
    if len(problemfiles) > 0:
        print ('Corruped Image Files:', problemfiles)
        f = open(os.path.join(dest, 'error_log.txt'), 'w')
        for i in problemfiles:
            f.write(i+'\n')
        f.close()
    print('Program Completed!!!', dir)
    return dest


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Elapsed Time: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

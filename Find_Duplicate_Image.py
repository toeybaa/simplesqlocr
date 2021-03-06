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
year = ''


def averagehash(file):
    """
    Calculate Image Hash based on input file
    Hashsize or image pixel can be set as comment below
    default hashsize is set by 10
    """
    try:
        with Image.open(file) as img:
            temp_hash = imagehash.dhash(img, 10) #put image pixel here: current = 10x10 pixel
    except PIL.UnidentifiedImageError:
        temp_hash = 'Corrupted Files'
        problemfiles.append(file)
    except Exception as e:
        temp_hash = str(e)
    return temp_hash


def readcsvfile():
    """
    Read CSV file as technicians selection list
    put the list of technicians each year when the program run
    column to be read in csv file can be set as comment below
    """
    user = []
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    title = 'CSV file for selecting user in ' + year
    file = filedialog.askopenfilename(title=title)
    print('Chosen CSV file:', file)
    with open(file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            user.append(row[1]) #set the row number as the column to read the csv file
    return (user)


def checkpath(path):
    """
    Check if the input path is existed or not
    """
    if not os.path.exists(path):
        os.makedirs(path)


def checkyear(year):
    """
    Check if the input year is within range of possibility or not
    """
    year = int(year)
    now = datetime.datetime.now()
    dateyear = now.year
    return year >= 2018 and year <= dateyear


def removecsv(path):
    """
    Remove existing csv file in the directory
    """
    if os.path.exists(path):
        os.remove(path)


def copy(path1, path2):
    """
    Copy file from path1 to path2 as same image different technician counter
    """
    if not os.path.exists(path2):
        os.makedirs(path2)
    shutil.copy(path1, path2)
    global d
    d += 1


def copycustomer(path1, path2):
    """
    Copy file from path1 to path2 as same image and same technician counter
    """
    if not os.path.exists(path2):
        os.makedirs(path2)
    shutil.copy(path1, path2)
    global customer_count
    customer_count += 1


def getcustomer(path):
    """
    Extract full filename to customer number only
    """
    str2 = os.path.sep
    res = path.split(str2, 16)[-1]
    str3 = '_'
    res = res.split(str3, 1)[-1]
    res = res.rsplit('_')[0]
    return res


def getmechanic(path):
    """
    Extract full filename to technician number only
    """
    str2 = os.path.sep
    res = path.split(str2, 16)[-1]
    str3 = '_'
    res = res.split(str3, 2)[-1]
    res = res.rsplit('_')[0]
    return res


def keepdup(ids):
    """
    List Manipulation: keep only duplicated element
    """
    return set(i for i in ids if ids.count(i) > 1)


def odd_occurring_num(arr):
    """
    List Manipulation: keep only distinct element
    """
    return [i for i in arr if arr.count(i) < 2]


def even_occurring_num(arr):
    """
    List Manipulation: keep only elements with have more than 2 occurrences
    """
    return [i for i in arr if arr.count(i) >= 2]


def calendar(path, years):
    """
    Calendar List generator: from 2018 to 2022
    """
    year = [2018, 2019, 2020, 2021, 2022] # add more years in future
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
        if (str)(years) == (str)(i) and years == 2022: # change year here
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
                    day = list(range(1, 29))# check February date count
                    for k in day:
                        k = str(k)
                        fpath.append((os.path.join(path, os.path.join(i, os.path.join(j, k)))))
    return (fpath)


def dupdict(dictA):
    """
    Dictionary manipulation: reversed dict and select only element with multiple key
    """
    dictB = {}
    for key, value in dictA.items():
        dictB.setdefault(value, set()).add(key)
    res = filter(lambda x: len(x) > 1, dictB.values())
    return (list(res))


def getpathhashcopy(path, path2):
    dir = 0
    opFolName = 'Image_Duplicate'
    opFolName2 = 'Customer_Duplicate'
    user = readcsvfile()
    y = int(year)
    imgfolder = calendar(path, y) #\2018\6\1, 2018\6\2
    user = set(user) #distinct user set
    print('Calculating Images Hash...')
    start = time.time()
    for a in imgfolder:
        c = 0
        print('Looking Images Folder', a, end=' >>> ')
        try:
            for file in os.listdir(a): # file = customer_mechanic_cusnumber_date.jpeg
                if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
                    for i in user: #8765234234 in cus_8765234234
                        if i in file:
                            path1 = os.path.join(a, file)
                            hashdict[path1] = averagehash(path1) #dict[key#3] = value
                            c += 1
        except OSError as e:
            print(e, end=' >>> ')
        if c != 0:
            print(c, 'suspect images hashed')
        if c == 0:
            print('No suspect images found')

    dupimglist = dupdict(hashdict)
    end = time.time()
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
    startcopy = time.time()
    nFolPath = os.path.join(path2, opFolName)
    nFolPath2 = os.path.join(path2, opFolName2)
    checkpath(nFolPath)
    checkpath(nFolPath2)
    csvfile1 = nFolPath + '_Result.csv'
    csvfile2 = nFolPath2 + '_Result.csv'
    removecsv(csvfile1)
    removecsv(csvfile2)
    mode1 = 'a' if os.path.exists(csvfile1) else 'w'
    mode2 = 'a' if os.path.exists(csvfile2) else 'w'
    csvheader = ['customer_number', 'technician_number', 'filename', 'hashvalue']
    f = open(csvfile1, mode1, newline='')
    writer = csv.writer(f)
    writer.writerow(csvheader)
    f2 = open(csvfile2, mode2, newline='')
    writer2 = csv.writer(f2)
    writer2.writerow(csvheader)
    for i in dupimglist:
        temp = str(hashdict.get(list(i)[0]))
        if '000000000000000000000000' in temp or '00c0500c0500c0301c0702c05' in temp\
                or '00000000000000000000000' in temp or '0000000000000000000000002' in temp or '0000000000000000000000400' in temp\
                or 'ffffffffffffffffffffffdff' in temp or 'ffffffffffffffffffffffff' in temp or '000000000000000000000' in temp:
            continue
            # eliminate black image by pixel result hash
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
                cus = getcustomer(j)
                mec = getmechanic(j)
                write = [cus, mec, j,temp]
                writer.writerow(write)
        if len(even_occurring_num(customer)) >= 2:
            ids = keepdup(customer)
            for j in file:
                if list(ids)[0] in j:
                    copycustomer(j, hashfolder2)
                    cus = getcustomer(j)
                    mec = getmechanic(j)
                    write = [cus, mec, j, temp]
                    writer2.writerow(write)
    print('Total Number of same images with different customer number:', d)
    print('Total Number of same images with same customer number:', customer_count)
    print('Successfully copied', d, 'images to', nFolPath)
    print('Successfully copied', customer_count, 'images to', nFolPath2)
    endcopy = time.time()
    hourscopy, remcopy = divmod(endcopy - startcopy, 3600)
    minutescopy, secondscopy = divmod(remcopy, 60)
    if d != 0:
        print("Copying Took: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hourscopy), int(minutescopy), secondscopy),
          '>>>', 'Per image:', str("{:.2f}".format(((endcopy - startcopy) / (d+customer_count)) * 1000)), 'ms')
    if d == 0:
        print("No Exact Image Duplicate Found!")
    if d >= 0:
        return True
    else:
        return False


def main():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    # folder = filedialog.askdirectory(title='Choose Source Folder')
    # folderout = filedialog.askdirectory(title='Choose Image Destination Folder')
    folder = r'W:\upload'
    folderout = r'E:\Python_Image_Out'
    global year
    if len(sys.argv) <= 1:
        year = str(input('Please input year to compare the image: '))
    else:
        year = str(sys.argv[1])
    flag = checkyear(year)
    while not flag:
        print('Year', year, 'was not found in image folder')
        year = int(input("Please choose year between 2018 and current year: "))
        if checkyear(year):
            break
    year = str(year)
    folderout = os.path.join(folderout, year)
    dir = getpathhashcopy(folder, folderout)
    dest = folderout
    if len(problemfiles) > 0:
        print ('Corruped Image Files:', problemfiles)
        f = open(os.path.join(dest, 'error_log.txt'), 'w')
        for i in problemfiles:
            f.write(i+'\n')
        f.close()
    print('Program Completed!!!', dir)
    input('Press Any Key To Close This Window...')
    return dest


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Elapsed Time: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

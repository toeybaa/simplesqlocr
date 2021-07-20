# -*- coding: utf-8 -*-
import csv
import os
# import pandas as pd


firstpath = r"C:\Users\patchnui\Downloads\Python_Test\Upload"
month = 12,12
day = 1,1
user = []

def readcsvfile():
    with open('Test_Python_LMR_122018.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            user.append(row[1])

def readimage():
    flag = False
    for i in month:
        i = str(i)
        fpath = os.path.join(firstpath, i)
        if flag:
            break
        flag = True
        for j in day:
            j = str(j)
            spath = os.path.join(fpath,j)
            return (str(spath)+'\\')

def printlist(a):
    for i in zip(a):
        print i

def main ():
    img = []
    dir = []
    readcsvfile()
    folder = readimage()
    for file in os.listdir(folder):
        if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
            img.append(file)

    for i in img:
        # print (i)
        for j in user:
            if j in i:
                dir.append(i)

    dir = list(dict.fromkeys(dir))
    printlist(dir)



if __name__ == "__main__":
	main()
# -*- coding: utf-8 -*-
import csv
import os
# import pandas as pd
import os
from tkinter import Tk, filedialog



firstpath = r"C:\Users\patchnui\Downloads\Python_Test\Upload"
imgfolder = []

def readcsvfile():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file = filedialog.askopenfilename()
    print ('Looking CSV file:',file)
    with open('Test_Python_LMR_122018.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            user.append(row[1])
        user.append('1004219015')
        user.append('82841053')
        user.append('1011233012')
        user.append('1012573006')

def readimage():
    flag = False
    for i in imgfolder:
        i = str(i)
        fpath = os.path.join(firstpath, i)
        if flag:
            break
        flag = True
        for j in day:
            j = str(j)
            spath = os.path.join(fpath,j)
            return (str(spath)+'\\')
# def readimage():
#     flag = False
#     for i in imgfolder:
#         i = str(i)
#         fpath = os.path.join(firstpath, i)
#         if flag:
#             break
#         flag = True
#         for j in day:
#             j = str(j)
#             spath = os.path.join(fpath,j)
#             return (str(spath)+'\\')

def listdirs(rootdir):
    for root, dirs, files in os.walk(rootdir):
        if not dirs:
            imgfolder.append(root)

def main (path):
    img = []
    dir = []
    readcsvfile()
    listdirs(path)
    for i in imgfolder:
        i = str(i)+'\\'
        for file in os.listdir(i):
            if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
                img.append(i+file)
        for i in img:
            for j in user:
                if j in i:
                    dir.append(i)
        dir = list(dict.fromkeys(dir))
        finaldir = dir
    return (finaldir)

if __name__ == "__main__":
    main()
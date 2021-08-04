import os
import shutil
from PIL import Image, ImageStat
import time
import hashlib
from tkinter import Tk, filedialog
import numpy as np
import imagehash

def	CreateFolderOut(imagePath):
	opFolName = 'Image_Duplicate'
	nFolPath = os.path.join(imgoutpath, opFolName)
	directory = os.path.dirname(nFolPath)
	if not os.path.exists(directory):
		os.makedirs(nFolPath)
	else:
		shutil.rmtree(nFolPath, ignore_errors=True)
		os.makedirs(nFolPath)
	return nFolPath

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

root = Tk()
root.withdraw()
root.attributes('-topmost', True)
firstpath = filedialog.askdirectory()
firstpath = 'W:\\Upload'
foundimg = []
imgoutpath = firstpath
opFolName = 'Image_Duplicate'
nFolPath = os.path.join(imgoutpath, opFolName)
from PIL import Image, ImageStat
from collections import Counter
import numpy as np
import time
import datetime

Img = ['Honda-Civic-Prototype-Modify - Copy.jpg', 'Honda-Civic-Prototype-Modify - Copy.jpg']
I1 = Img[0]
I2 = Img[1]
print ('I1',I1)
ref_img_1 = Image.open(I1)
ref_img_arr_1 = np.asarray(ref_img_1)
flat_array_1 = ref_img_arr_1.flatten()
RH1 = Counter(flat_array_1)
H1 = []
for i in range(256):
	if i in RH1.keys():
		H1.append(RH1[i])
	else:
		H1.append(0)
ref_img_2 = Image.open(I2)
ref_img_arr_2 = np.asarray(ref_img_2)

flat_array_2 = ref_img_arr_2.flatten()
RH2 = Counter(flat_array_2)
H2 = []

for i in range(256):
	if i in RH2.keys():
		H2.append(RH2[i])
	else:
		H2.append(0)

def L2Norm(H1,H2):
	distance =0
	for i in range(len(H1)):
		temp = int(H1[i])-int(H2[i])
		distance += int(np.square(temp))
	result = np.sqrt(distance)
	if result <= 100:
		return True
	else: return False


def main():
	global I1
	global I2
	print (I1)
	I1 = 'Honda-Civic-Prototype-Modify - Copy2.jpg'
	I2 = 'Honda-Civic-Prototype-Modify - Copy.jpg'

	print (L2Norm(H1, H2))

def compare():
	start1 = datetime.datetime.now()
	for i in range(2000):
		main()
		# print('Main I1', I1)
	end1 = datetime.datetime.now()
	time_elapsed1 = end1 - start1
	print (time_elapsed1)


if __name__ == "__main__":
	# start = datetime.datetime.now()
	# meanImg()
	# end = datetime.datetime.now()
	# time_elapsed = end - start
	# print ('Time Used:',time_elapsed.microseconds, 'us')
	compare()
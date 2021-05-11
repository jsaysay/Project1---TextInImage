"""


Description - 	This program will extract the text from an 
				Image and print it to the terminal.
				see readme.txt file for use.
"""
from PIL import Image
import sys
import math

imageName = sys.argv[1]
#open image
img = Image.open(imageName)
#convert image pixels into 1d array of tuples (R,G,B).
flatImage = img.getdata()
#index of last pixel of the image
lastIndex = len(flatImage)
#variable to store string representation of data size.
strSize = ""

#get size of message by reading the bottom right 11 pixels
for i in reversed(range(lastIndex - 11, lastIndex)):
	for j in range(3):
		if not((i == lastIndex - 11) and (j == 2)):
			strSize += str(flatImage[i][j] % 2)

#convert string representation of data size to Int
dataSize = (int(strSize,2))
#number of pixels the data is embedded in.
pixelNumber = math.ceil(dataSize/3)

#indexes where the data is stored.
dataEndIndex = lastIndex - 11
dataBeginIndex = dataEndIndex - pixelNumber 

#store each 8 bits of data in as a string.
eightBitStrData = ""
#variable to store all the data.
finalMessage = ""
#count to keep track of each 8 bits of data
count = 0

#extract message from pixels
for i in reversed(range(dataBeginIndex,dataEndIndex)):
	for j in range(3):
		eightBitStrData += str(flatImage[i][j] % 2)
		count += 1
		if count == 8:
			finalMessage += chr(int(eightBitStrData,2))
			count = 0
			eightBitStrData = ""

print(finalMessage)
img.close()

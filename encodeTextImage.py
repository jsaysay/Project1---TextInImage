"""
Name:Jonathan Saysay

Class: CS353

Description - 	This program will embed text into an image
				see readme.txt file for use.
"""

from PIL import Image
import sys
import math

imageName = sys.argv[1]
imageData = sys.stdin.read()
#open image
img = Image.open(imageName)
#get data size
imageDataSize = len(imageData) * 8
#flatImage will contain all pixels in an array.
flatImage = img.getdata()
endIndex =  len(flatImage)
#variable for holding 32 bit binary representation of data size.
strData = ""
#convert size of data from int to 32 bit string representation of size.
strData = bin(imageDataSize).lstrip("-0b").zfill(32)
#dataArr will contain all the pixels of the image with embedded text and size.
dataArr = []
#pixelArr is a temporary variable for holding 1 pixel at a time.
pixelArr = []
#index for the 32 bit string.
index = 0

#embed text size into bottom right 11 pixels.
for i in reversed(range(endIndex - 11, endIndex)):
	for j in range(3):
		if not((i == endIndex - 11) and (j == 2)):
			if strData[index] == "0":
				if flatImage[i][j] % 2 == 1:
					pixelArr.append(flatImage[i][j] - 1)
				else:
					pixelArr.append(flatImage[i][j])
			else:
				if flatImage[i][j] % 2 == 0:
					pixelArr.append(flatImage[i][j] + 1)
				else:
					pixelArr.append(flatImage[i][j])
		else:
			pixelArr.append(flatImage[i][j])

		index += 1

	dataArr.append((pixelArr[0],pixelArr[1],pixelArr[2]))
	pixelArr.clear()

#amount of pixels needed to embed data.
pixelNumber =  math.ceil(imageDataSize/3)

#indexes from  the 12th pixel to pixel based on data size.
dataEndIndex = endIndex - 11
dataBeginIndex = dataEndIndex - pixelNumber

#store binary representation for a character of the data.
charData = bin(ord(imageData[0])).lstrip("0b").zfill(8)
dataIndex = 0
charIndex = 0

#embed message data onto pixels starting with 12th pixel.
for i in reversed(range(dataBeginIndex,dataEndIndex)):
	for j in range(3):
		if not(i == dataBeginIndex and dataIndex == len(imageData) - 1 and charIndex == 8):
			if charData[charIndex] == "0":
				if flatImage[i][j] % 2 == 1:
					pixelArr.append(flatImage[i][j] - 1)
				else:
					pixelArr.append(flatImage[i][j])
			else:
				if flatImage[i][j] % 2 == 0:
					pixelArr.append(flatImage[i][j] + 1)
				else:
					pixelArr.append(flatImage[i][j])

			charIndex += 1
			if charIndex == 8 and dataIndex != len(imageData) - 1:
				dataIndex += 1
				charData = bin(ord(imageData[dataIndex])).lstrip("0b").zfill(8)
				charIndex = 0
		else:
			pixelArr.append(flatImage[i][j])

	dataArr.append((pixelArr[0],pixelArr[1],pixelArr[2]))
	pixelArr.clear()

#append remaining unchanged pixels into our data for the image.
for i in reversed(range(0,dataBeginIndex)):
	dataArr.append(flatImage[i])

#put all data into the image.
img.putdata(list(reversed(dataArr)))

imageName = imageName.split(".")[0]
img.save(imageName + ".png")
img.close()

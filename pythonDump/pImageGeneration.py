import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
strFolImage = os.getcwd() + '\\test_image'
listImageFile = list()
strTest = str()
#listWellId = list()
listMap = list()
listTupleMap = list()
listTextToPrint = list()
listUnmappedWell = list()
listImageTestValue = list()
listImage = list()
listText = list()
listImageSubText = list()
boolMappedSuccessful = bool(False)
intImageCount = 0
for i in os.listdir("C:\\pierre\\apps\\python apps\\echolumena\\connection\\test_image"):
	if 'welltestmapping' in i:
		strFileTestMapping = strFolImage + '\\' + i
		strTest = i.split('-')[-2]
	if i[-4:] == '.jpg' and 'test' not in i:
		listImageFile.append(strFolImage + '\\' + i)
#		listWellId.append(i.split('-')[-1][:2])
#		print(i)

#print(listWellId)
with open(strFileTestMapping,"r") as fileWellMap:
	listMap = fileWellMap.read().split('\n')
for i in listMap:	
	print(i)
	listTupleMap.append(i[2:-2].split('\', \''))
#print(listTupleMap)

for i in listImageFile:
	for j in listTupleMap:
		if i.split('-')[-1][:2] in j:
#			print(i,'mapped to',j)
			boolMappedSuccessful = True
			listImageTestValue.append([i,j])
	if boolMappedSuccessful == False:
		listUnmappedWell.append(i)
	boolMappedSuccessful = False

#print(listUnmappedWell)

for i in listUnmappedWell:
	listImageTestValue.append([i,[i.split('-')[-1][:2],'N/A','N/A']])

for i in listImageTestValue:
	print(i)




listImage = [Image.open(i[0]) for i in listImageTestValue]
listText = [i[1][1]+'\n'+i[1][2] for i in listImageTestValue]

print(listText)


widths, heights = zip(*(i.size for i in listImage))

total_width = sum(widths)
max_height = max(heights)
imgSubText = Image.new('RGB', (int(total_width),max_height*3), (242, 242, 242))
x_offset = 0
for element in listImageTestValue:
	print('element = ',element[0])
	i = element[1][1] + ' ' + element[1][2]
	print(i)
	if 'N/A' not in i:
		fontSubImage = ImageFont.truetype("arial.ttf",size=max_height/6)
#		imgSubText = Image.new('RGB', (int(total_width/len(listText)),max_height*2), (242, 242, 242))
#		imgSubText = Image.new('RGB', (int(total_width),max_height*2), (242, 242, 242))
		dSubText = ImageDraw.Draw(imgSubText)
		listImageSubText.append(dSubText)
		font_width, font_height = fontSubImage.getbbox(i)[-2:]
		intWidthSubText = (int(total_width/len(listText)) - font_width) / 2
		intHeightSubText = (max_height - font_height) / 2
		dSubText.text((intWidthSubText + x_offset, intHeightSubText + max_height), i, fill=(0,0,0), font=fontSubImage)
		imageElement = Image.open(element[0])
		imgSubText.paste(imageElement,(x_offset,max_height*2))
		intImageCount = intImageCount + 1
		x_offset += imageElement.size[0]
#		imgSubText.save(strFolImage + '\\' + element[1][1] + str(intImageCount) + '.jpg')
fontUpperText = ImageFont.truetype("arial.ttf",size=max_height/2)
dUpperText = ImageDraw.Draw(imgSubText)
font_width, font_height = fontUpperText.getbbox(strTest)[-2:]
new_width = (total_width - font_width) / 2
new_height = (max_height - font_height) / 2
dUpperText.text((new_width, new_height), strTest, fill=(0,0,0), font=fontUpperText)
imgSubText.save(strFolImage + '\\' + 'fullImage' + '.jpg')
intImageCount = 0
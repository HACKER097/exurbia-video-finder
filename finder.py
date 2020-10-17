import os
import platform
#importing stuff

platform = platform.system()
#identifying the OS 

if platform == "Linux":
	os.system('ls >> names.txt')
elif platform == "Windows":
	os.system('dir /b *.vtt > names.txt')
elif platform == "Darwin":
	os.system('ls >> names.txt')
#Putting filenames in a text file for each OS

names = open("names.txt", 'r+')
menu = names.readlines(1000000)
names.truncate(0)
filenames = []
printed = []
findwhat = input("WHAT WORD ARE U LOOKING FOR: ").split()

for i in range(len(menu)):

	filenames.append(menu[i].replace('\n',''))

for i in range(len(filenames)):

	with open(filenames[i],'r',encoding="utf-8") as file: 
		
		for line in file: 

			for word in line.split():
				for x in range(len(findwhat)):

					if word.lower() == findwhat[x].lower():
						printed.append(filenames[i])

for element in set(printed):
	print(element)
if len(printed) == 0:
	print("Nothing found")


import os

os.system('ls ~/subs >> names.txt')
names = open("names.txt", 'r+')
menu = names.readlines(1000000)
names.truncate(0)
filenames = []
printed = []
findwhat = input("WHAT WORD ARE U LOOKING FOR: ").split()

for i in range(len(menu)):

	filenames.append(menu[i].replace('\n',''))

for i in range(len(filenames)):

	with open(filenames[i],'r') as file: 
		
		for line in file: 

			for word in line.split():
				for x in range(len(findwhat)):

					if word == findwhat[x]:
						print(filenames[i])


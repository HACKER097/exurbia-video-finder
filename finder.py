import os
import platform
from pathlib import Path
import re
#importing stuff

# returns a string array of the absolute path of all subtitle files in the working directory
def findAllSubtitleFiles():
	subtitleFiles = []
	workingDirectory = Path('.')
	for childDir in workingDirectory.iterdir():
		if childDir.name.endswith('.vtt'):
			subtitleFiles.append(childDir.absolute())
	return subtitleFiles

#grabs the start timestamp of a line
def startTimestampOfLine(line):
	pattern = re.compile("^\d\d:\d\d:\d\d.\d\d\d")
	result = re.search(pattern, line)
	try:
		return result.group(0)
	except AttributeError:
		return line

# does a given string contain all the words?
def strContainsAllWords(str, words):
	wordCount = 0
	for s in str.rsplit(" "):
		for word in words:
			if s.lower().replace(","," ") == word:
				wordCount = wordCount + 1
	return wordCount == len(words)

# does a given string contain some of the words?
def strContainsAnyWord(str, words):
	for s in str.rsplit(" "):
		for word in words:
			if s == word:
				return True
	return False

#returns an array of lines in the given file if the predicate is true
#predicate parameters are (String, String[])
# String being the line that the predicate is checking
# String[] is the list of words that we want to compare
def linesInFile(file, words, predicate):
	foundLines = []
	file = open(filename, "r", encoding="utf-8")
	previousLine = ""
	for line in file:
		if predicate(line, words):
			foundLines.append("At: " + startTimestampOfLine(previousLine) + " -- "+ line)
		previousLine = line
	return foundLines

while True:
	filenames = findAllSubtitleFiles()
	findwhat = input("WHAT WORD ARE U LOOKING FOR: ").rsplit(" ")
	print()
	print("######################################")
	print()


	for filename in filenames:
		with open(filename, "r", encoding="utf-8") as file:
			lines = linesInFile(file, findwhat, strContainsAllWords)
			if len(lines) > 0:
				stringCutLength = len(str(Path.cwd())) + 1
				name = str(filename)[stringCutLength:][:-19]
				link = str(filename)[stringCutLength:][-18:][:-7]
				print("Word(s) found in the video: " + name)
				print()
				for line in lines:
					print(line)
					line = line[:12].split(":")
					try:
						time = round(int(line[2])*60 + float(line[3]))
						print("youtube link : https://youtube.com/watch?v=" + link + "&t=" + str(time) + "s")
					except IndexError:
						print("***WORKING ON A FIX FOR LINK***")

					print()
					print("######################################")
					print()


	print("END OF LIST")

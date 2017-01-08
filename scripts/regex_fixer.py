import os
import re

linkRegex = r"(?!_|\*).\[([^\[]+)\]\(([^\)]+)\)"
linkBoldRegex = r"\[([^\[]+)\]\(([^\)]+)\)\*\*"
fixBugs = r"line-numbers=off, "

for file in os.listdir("manuscript"):
    if file.endswith(".txt"):
        with open("manuscript/" + file) as f:
            fileData = ""
            fileContent = f.readlines()
            for line in fileContent:
                line = re.sub(fixBugs, r'', line.rstrip())
                fileData += line + "\n"

            text_file = open("manuscript/" + file, "w")
            text_file.write(fileData)
            text_file.close()
print "Book updated!"
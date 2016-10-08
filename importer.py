#!/usr/bin/env python
# encoding: utf-8
import re

myfile = open('Raw_OnTheRoad.txt', 'r')
data = myfile.read()
myfile.close()

# We're going to remove all the numbers from the text to get rid of the page numbers. Wonder if there are any false positives?
spacelines = r"\d"
output = re.sub(spacelines, '', data)

# Next we'll remove any of the three-newline blocks leftover from stripping out the page numbers, and replace them with a single space. Some of these (all?) look like double spaces and we should fix that later.
output = output.replace('\n\n\n', ' ')
print "OK I removed the page numbers and newlines."

# Let's write the output to a file, which should end up with paragraph-length lines, mostly single-spaced.
outputfile = open('otr_import.txt', 'w')
outputfile.write(output)
print "OK I wrote the output to your file."

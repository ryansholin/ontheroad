#!/usr/bin/env python
# encoding: utf-8
import textblob
from textblob import TextBlob
from textblob import Word


myfile = open('otr_output.txt', 'r')
data = myfile.read()
myfile.close()

text = TextBlob(data)

txtfile = open('checkinated.txt', 'a')
for word in text.words:
    checkinated = word.spellcheck()
    confylist = [x[1] for x in checkinated]
    wordlist = [x[0] for x in checkinated]
    confidence = confylist[0]
    if confidence == 1 and word[0].islower():
        txtfile.write(word + "|" + str(checkinated[0]) + "\n")
        print "word logged"
txtfile.close()
print "Spellcheck complete."

# Simple extended boolean search engine: indexer based on cranfield format
# Hussein Suleman
# 21 April 2016

import os
import re
import sys

import porter

import parameters

# check parameter for collection name
if len(sys.argv)==1:
   print ("Syntax: index.py <collection>")
   exit(0)
collection = sys.argv[1]

# read and parse input data - extract words, identifiers and titles
#f = open (collection, "r")
identifier = ''
document = ''
title = ''
indocument = False
intitle = False
data = {}
titles = {}

for fname in os.listdir(collection):
        if fname.split(".")[0]=="document":
           with open(collection+"/"+fname, encoding="ascii",errors="surrogateescape") as f:
              #print (fname)
              #get the document number
              doc_number = fname.split(".")[1]
              
              lines = f.read().replace('\n', '')
              
              data[doc_number]=lines
              titles[doc_number] = fname

# document length/title file
g = open (collection + "_index_len", "w")

# create inverted files in memory and save titles/N to file
index = {}
N = len (data.keys())
p = porter.PorterStemmer ()

#data contains the document key value pairs.
#key is the file name and value the lines in the file
for key in data:
    content = re.sub (r'[^ a-zA-Z0-9]', ' ', data[key])
    content = re.sub (r'\s+', ' ', content)
    words = content.split (' ')
    doc_length = 0
    #if key=="1":
       #print ("array: ",words)
    for word in words:
        if word != '':
            #convert to lower case first
            word = word.lower()
            if parameters.stemming:
                word = p.stem (word, 0, len(word)-1)
            #if word == "avl" or word == "Avl":
               #print ("doc with avl: ",key)
            doc_length += 1
            if not word in index:
                index[word] = {key:1}
            else:
                if not key in index[word]:
                    index[word][key] = 1
                else:
                    index[word][key] += 1
    print (key, doc_length, titles[key], sep=':', file=g)

# document length/title file
g.close ()

# write inverted index to files
try:
   os.mkdir (collection+"_index")
except:
   pass

#the key is the word
for key in index:
    #print ("key: ",key)
    try:
       f = open (collection+"_index/"+key, "w")
       #the entry is the document number
       for entry in index[key]:
          print (entry, index[key][entry], sep=':', file=f)
       f.close ()
    except:
       pass

# write N
f = open (collection+"_index_N", "w")
print (N, file=f)
f.close ()
    

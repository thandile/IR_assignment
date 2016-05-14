# Simple extended boolean search engine: query module
# Hussein Suleman
# 14 April 2016

import re
import math
import sys
import os

import porter

import parameters

# check parameter for collection name
if len(sys.argv)<3:
   print ("Syntax: index.py <collection> <query>")
   exit(0)
 
# construct collection and query
collection = sys.argv[1]
query = ''
arg_index = 2
while arg_index < len(sys.argv):
   query += sys.argv[arg_index] + ' '
   arg_index += 1

# clean query
if parameters.case_folding:
   query = query.lower ()
query = re.sub (r'[^ a-zA-Z0-9]', ' ', query)
query = re.sub (r'\s+', ' ', query)
query_words = query.split (' ')

# create accumulators and other data structures
accum = {}
filenames = []
p = porter.PorterStemmer ()

# get N
f = open (collection+"_index_N", "r")
N = eval (f.read ())
f.close ()

# get document lengths/titles
titles = {}
f = open (collection+"_index_len", "r")
lengths = f.readlines ()
f.close ()

# get index for each term and calculate similarities using accumulators
for term in query_words:
    if term != '':
        if parameters.stemming:
            term = p.stem (term, 0, len(term)-1)
        if not os.path.isfile (collection+"_index/"+term):
           print ("term not found: ",term)
           continue
        f = open (collection+"_index/"+term, "r")
        lines = f.readlines ()
        idf = 1
        if parameters.use_idf:
           #df is document frequency, documents which contains the term
           df = len(lines)

           #inverse df is to give preference to term with less document appearance
           idf = 1/df
           if parameters.log_idf:
              idf = math.log (1 + N/df)
        #lines with document and number of occurences of the term
        for line in lines:
            #print ("documents with term: ",line)
            mo = re.match (r'([0-9]+)\:([0-9\.]+)', line)
            if mo:
                file_id = mo.group(1)

                #term frequency is the number of terms in the document
                tf = float (mo.group(2))

                if not file_id in accum:
                    accum[file_id] = 0
                if parameters.log_tf:
                    tf = (1 + math.log (tf))
                accum[file_id] += (tf * idf)
                
        f.close()

# parse lengths data and divide by |N| and get titles
for l in lengths:
   mo = re.match (r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
   #print ("after mo ",mo)
   if mo:
      document_id = mo.group (1)
      length = eval (mo.group (2))
      title = mo.group (3)
      if document_id in accum:
         if parameters.normalization:
            accum[document_id] = accum[document_id] / length
         titles[document_id] = title

# print top ten results
result = sorted (accum, key=accum.__getitem__, reverse=True)
for i in range (min (len (result), 15)):
   print ("{0:10.8f} {1:5} {2}".format (accum[result[i]], result[i], titles[result[i]]))

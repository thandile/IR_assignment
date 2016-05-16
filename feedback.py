# Simple extended boolean search engine: Blind Feedback module
# Takunda Chirema
# 14 May 2016

import re
import math
import sys
import os

import porter

import parameters

p = porter.PorterStemmer ()
data = {}
doc_freq = {}
term_scores = {}
term_weights = {}

def term_finder (documents,collection,exclude):
    
    for doc_num in documents:
        doc = "document."+doc_num
        with open(collection+"/"+doc, encoding="ascii",errors="surrogateescape") as f:
            #print (fname)
            #get the document number
            #doc_number = fname.split(".")[1]
            lines = f.read().replace('\n', '')
            data[doc_num]=lines

    #put the terms of the feedback documents in df dictionary
    #the key is the term and value number of feedback documents it appears in
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
            #doc_length += 1
            if not word in doc_freq:
                doc_freq[word] = 1
            else:
                doc_freq[word] += 1

    f = open (collection+"_index_N", "r")
    N = eval (f.read ())
    f.close()
    
    for term in doc_freq:
        #idf = math.log (1 + N/df)

        #check that the term exists in the inverted files else drop it
        if (term not in exclude) and (os.path.isfile (collection+"_index/"+term) ):
           score1 = math.log (1 + doc_freq[term] )

           #get number of lines/documents the term appears in
           df = sum(1 for line in open(collection+"_index/"+term))
           score2 = math.log (1 + N/df)

           score = score1*score2

           term_scores[term] =score

    sorted_scores = sorted (term_scores, key=term_scores.__getitem__, reverse=True)
    top_score = term_scores[sorted_scores[0]]

    for i in range (1,5):
        term = sorted_scores[i]
        print ("feedback term:",term," score:",term_scores[term])
        term_weights[term] = parameters.feedback_weight*(term_scores[term]/top_score)

    return term_weights

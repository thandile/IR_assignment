# Simple extended boolean search engine: query module
# Hussein Suleman
# 14 April 2016

import re
import math
import sys
import os
import irndcg
import irmap
import porter
import time
import stop

import parameters

import feedback

# check parameter for collection name
if len(sys.argv)<3:
   print ("Syntax: index.py <collection> <query>")
   exit(0)

# construct collection and query
collection = sys.argv[1]
query = ''
query_file = ''   #search using the query file ".\testbeds\testbed6\query.1"
arg_index = 2
while arg_index < len(sys.argv):
    query_file += sys.argv[arg_index] + ' '
    f = open(query_file, "r")
    query = f.readline()
    f.close()
    arg_index += 1

# clean query
if parameters.case_folding:
   query = query.lower ()
query = re.sub (r'[^ a-zA-Z0-9]', ' ', query)
query = re.sub (r'\s+', ' ', query)
query_words = query.split (' ')
query_id = query_file.split(".")[-1]
print("queryid:",query_id)
# create accumulators and other data structures
accum = {}
filenames = []
p = porter.PorterStemmer()
feedback_weights = {}
original_query_words = []
relevant_doc_ids = []  #used to search in the relevance documents
# get N
f = open (collection+"_index_N", "r")
N = eval (f.read ())
f.close ()

# get document lengths/titles
titles = {}
f = open (collection+"_index_len", "r")
lengths = f.readlines ()
f.close ()

def initial_feedback_weights():
   print ("query feedback: ",parameters.feedback,"incremental:",parameters.incremental_feedback,"positional:",parameters.positional_feedback)
   #time.sleep(5.5)
   for term in query_words:
      original_query_words.append(term)
      if parameters.stemming:
         term = p.stem (term, 0, len(term)-1)
      feedback_weights[term] = 1
      #print ("initial q:",term," feedback:",feedback_weights[term])

def query():
   # get index for each term and calculate similarities using accumulators
   for term in query_words:
       if term != '' and (term not in stop.stop_words):
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
                   #Other feedback terms with have smaller weights to avoid diversion from original query
                   #print("term:",term)
                   accum[file_id] += feedback_weights[term]*(tf * idf)
                   #print("score:",accum[file_id],"tf:",tf,"idf:",idf,"tf*idf",str(tf*idf))
				   
           f.close()

def parse_lengths():
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



def get_feedback(doc_num):

   result = sorted (accum, key=accum.__getitem__, reverse=True)

   #get feedback terms
   fb_documents={}
   for i in range (min (len (result), doc_num)):
      fb_documents[result[i]] = accum[result[i]]

   #print("params for feedback: ",str(fb_documents),"***",str(original_query_words),"***",str(collection))
   feedback_term_weights = feedback.term_finder(fb_documents,collection,original_query_words)

   #add the terms to the weights
   for term in feedback_term_weights:
      weight = feedback_term_weights[term]
      
      if parameters.stemming:
         term = p.stem (term, 0, len(term)-1)

      #print ("term:",term,"weight: ",str(weight))
      
      if term in feedback_weights:
         feedback_weights[term] += weight
      else:
         feedback_weights[term] = weight
         query_words.append(term)

def print_results():
   # print top ten results
   result = sorted (accum, key=accum.__getitem__, reverse=True)

   for i in range (min (len (result), 15)):
      print ("{0:10.8f} {1:5} {2}".format (accum[result[i]], result[i], titles[result[i]]))
      relevant_doc_ids.append((result[i]))

def run_query():
   initial_feedback_weights()

   query()

   parse_lengths()

   if parameters.feedback:

      if (parameters.incremental_feedback):
         for i in range (1,parameters.feedback_iterations+1):
            print("getdocs: ",str(parameters.feedback_documents*i))
            get_feedback(parameters.feedback_documents*i)

         #sort the feedback parameters and get only the terms in parameters.terms
         result = sorted (feedback_weights, key=feedback_weights.__getitem__, reverse=True)

         for i in range (min (len (result), parameters.feedback_terms),len(result)):
            try:
               #print("removed:",result[i])
               query_words.remove(result[i])
            except:
               pass

         for term in feedback_weights:
            if term not in original_query_words:
               feedback_weights[term] = feedback_weights[term]/parameters.feedback_iterations
               if term in query_words:
                  print ("incremental feedback terms:",term," score:",feedback_weights[term])
      else:
         get_feedback(parameters.feedback_documents)

      query()

      parse_lengths()

   print_results()

   returned = []
   returned.append(irndcg.irndcg(query_id, relevant_doc_ids, query_file))
   returned.append( irmap.irmap(query_id, relevant_doc_ids, query_file) )

   return returned

idcg_map = run_query()
f = open ("query_results.txt", "w")
print (str(idcg_map[0])+"\n"+str(idcg_map[1]), file=f)
f.close ()



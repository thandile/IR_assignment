# Simple extended boolean search engine: query module
# Hussein Suleman
# 14 April 2016

import re
import math
import sys
import os
import irndcg
import porter
import sys
import subprocess
import time

import parameters

import feedback

# check parameter for collection name
if len(sys.argv)==1:
   print ("Syntax: results.py <collection>")
   exit(0)
collection = sys.argv[1]

def start():
   #parameters.feedback = False
   print ("feedback: ",parameters.feedback,"incremental:",parameters.incremental_feedback,"positional:",parameters.positional_feedback)
   #time.sleep(5.5)
   run("results/with_2_feedback_iterations")



def run(output):
   testbed_scores = {}
   total_mean_map = 0
   total_mean_ndcg = 0
   for folder in os.listdir(collection):
      subprocess.call([sys.executable,'query.py',".\\"+collection+"\\"+folder+"\\",collection+"\\"+folder+"\\query.1"])
      f = open ("query_results.txt", "r")
      result = f.readlines()
      r1=[]
      r1.append (float(result[0].rstrip()))
      r1.append (float(result[1].rstrip()))
      print("R1: "+str(r1))

      subprocess.call([sys.executable,'query.py',".\\"+collection+"\\"+folder+"\\",collection+"\\"+folder+"\\query.2"])
      f = open ("query_results.txt", "r")
      result = f.readlines()
      r2=[]
      r2.append (float(result[0].rstrip()))
      r2.append (float(result[1].rstrip()))
      print("R2: "+str(r2))
      
      subprocess.call([sys.executable,'query.py',".\\"+collection+"\\"+folder+"\\",collection+"\\"+folder+"\\query.3"])
      f = open ("query_results.txt", "r")
      result = f.readlines()
      r3=[]
      r3.append (float(result[0].rstrip()))
      r3.append (float(result[1].rstrip()))
      print("R3: "+str(r3))
      
      subprocess.call([sys.executable,'query.py',".\\"+collection+"\\"+folder+"\\",collection+"\\"+folder+"\\query.4"])
      f = open ("query_results.txt", "r")
      result = f.readlines()
      r4=[]
      r4.append (float(result[0].rstrip()))
      r4.append (float(result[1].rstrip()))
      print("R4: "+str(4))
      
      subprocess.call([sys.executable,'query.py',".\\"+collection+"\\"+folder+"\\",collection+"\\"+folder+"\\query.5"])
      f = open ("query_results.txt", "r")
      result = f.readlines()
      r5=[]
      r5.append (float(result[0].rstrip()))
      r5.append (float(result[1].rstrip()))
      print("R5: "+str(r5))

      mean_map = (r1[1]+r2[1]+r3[1]+r4[1]+r5[1])/5
      mean_ndcg = (r1[0]+r2[0]+r3[0]+r4[0]+r5[0])/5

      testbed_scores[folder] = {}
      testbed_scores[folder]["map"] = mean_map
      testbed_scores[folder]["ndcg"] = mean_ndcg

      total_mean_map += mean_map
      total_mean_ndcg += mean_ndcg

      print("mean_map:",mean_map)
      print("mean_ndcg:",mean_ndcg)

   overall_mean_map = total_mean_map/len(testbed_scores)
   overall_mean_ndcg = total_mean_ndcg/len(testbed_scores)

   f = open (output, "w")
   print ("MAP,"+str(overall_mean_map)+"\n"+"IDCG,"+str(overall_mean_ndcg), file=f)
   f.close ()

start()
         

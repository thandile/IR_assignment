import sys
import subprocess
import os

for folder in os.listdir("testbeds"):
    print(folder)
    if folder!=".DS_Store":
        subprocess.call(["python", "index.py",".\\testbeds\\"+folder+"\\"])
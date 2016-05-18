import sys
import subprocess
import os

for folder in os.listdir("testbeds"):
    print(folder)
    subprocess.call(["python", "index.py",".\\testbeds\\"+folder+"\\"])